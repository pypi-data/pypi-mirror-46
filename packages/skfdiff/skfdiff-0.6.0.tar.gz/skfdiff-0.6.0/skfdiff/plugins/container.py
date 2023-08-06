#!/usr/bin/env python
# coding=utf-8

import json
import logging
import warnings
from functools import wraps
import uuid
from collections import deque, namedtuple
from typing import Union
import threading

import yaml
from loguru import logger
from path import Path
from streamz import collect
from xarray import concat, open_dataset, open_mfdataset

FieldsData = namedtuple("FieldsData", ["data", "metadata"])


@wraps(open_dataset)
def _safe_open_dataset(*args, **kwargs):
    with open_dataset(*args, **kwargs) as ds:
        data = ds.copy()
    return data


@wraps(open_mfdataset)
def _safe_open_mfdataset(*args, **kwargs):
    with open_mfdataset(*args, **kwargs) as ds:
        data = ds.compute().copy()
    return data


class AttrDict(dict):
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self


def coerce_attr(key, value):
    value_type = type(value)
    if value_type in [int, float, str]:
        return value
    for cast in (int, float, str):
        try:
            value = cast(value)
            logger.debug(
                "Illegal netCDF type ({}) of attribute for {}, "
                "casted to {}".format(value_type, key, cast)
            )
            return value
        except TypeError:
            pass
    raise TypeError(
        "Illegal netCDF type ({}) of attribute for {}, "
        "auto-casting failed, tried to cast to "
        "int, float and str"
    )


class Container:
    def __init__(
        self,
        path=None,
        mode="a",
        *,
        save="all",
        metadata={},
        force=False,
        nbuffer=None,
        save_interval=None
    ):
        if save_interval is None and nbuffer is None:
            save_interval = 10
        if save_interval is not None and nbuffer is not None:
            raise ValueError("You should provide either nbuffer or save_interval.")
        self.nbuffer = nbuffer
        self.save_interval = save_interval
        self._mode = mode
        self._metadata = metadata
        self.save = save
        self._cached_data = deque([], self._n_save)
        self._collector = None
        self._count_iter = 0
        self.path = path = Path(path).abspath() if path else None
        self._writer_thread_name = "writer_%s" % uuid.uuid1()

        if not path:
            return

        if self._mode == "w" and force:
            path.rmtree_p()

        if self._mode == "w" and not force and path.exists():
            raise FileExistsError(
                "Directory %s exists, set force=True to override it" % path
            )

        if self._mode == "r" and not path.exists():
            raise FileNotFoundError("Container not found.")
        path.makedirs_p()

        with open(self.path / "metadata.yml", "w") as yaml_file:
            yaml.dump(self._metadata, yaml_file, default_flow_style=False)

    @property
    def save(self):
        return "last" if self._n_save else "all"

    @save.setter
    def save(self, value):
        if value == "all":
            self._n_save = None
        elif value == "last" or value == -1:
            self._n_save = 1
        else:
            raise ValueError(
                'save argument accept only "all", "last" or -1 '
                "as value, not %s" % value
            )

    def _expand_fields(self, t, fields):
        fields = fields.assign_coords(t=t).expand_dims("t")
        for key, value in self._metadata.items():
            fields.attrs[key] = coerce_attr(key, value)
        self._cached_data.append(fields)
        return fields

    def _concat_fields(self, fields):
        if fields:
            return concat(fields, dim="t")

    def connect(self, stream):
        def get_t_fields(simul):
            return simul.t, simul.fields

        def expand_fields(inps):
            return self._expand_fields(*inps)

        def get_last(list_fields):
            try:
                return list_fields[-1]
            except IndexError:
                pass

        accumulation_stream = stream.map(get_t_fields).map(expand_fields)
        self._collector = collect(accumulation_stream)
        if self.save == "all":
            self._collector.map(self._concat_fields).sink(self._bg_write)
        else:
            self._collector.map(get_last).sink(self._bg_write)

        if self.nbuffer is not None:
            (accumulation_stream.partition(self.nbuffer).sink(self._collector.flush))
        if self.save_interval is not None:
            (
                accumulation_stream.timed_window(self.save_interval)
                .filter(bool)
                .sink(self._collector.flush)
            )

        return self._collector

    @property
    def writers(self):
        return [
            thread
            for thread in threading.enumerate()
            if thread.name == self._writer_thread_name
        ]

    @property
    def is_writing(self):
        if self.writers:
            return True
        return False

    def flush(self):
        if self._collector:
            self._collector.flush()
            while self.is_writing:
                pass

    def _write(self, concatenated_fields):
        if concatenated_fields is not None and self.path:
            len_concat_fields = concatenated_fields.t.size
            target_file = (
                self.path
                / "data_%i-%i.nc"
                % (self._count_iter, self._count_iter + len_concat_fields - 1)
            )
            self._count_iter = len_concat_fields + self._count_iter
            concatenated_fields.to_netcdf(target_file)
            concatenated_fields.close()
            self._cached_data = deque([], self._n_save)
            if self.save == "last":
                [
                    file.remove()
                    for file in self.path.glob("data_*.nc")
                    if file != target_file
                ]

    def _bg_write(self, concatenated_fields):
        thread = threading.Thread(
            name=self._writer_thread_name,
            target=self._write,
            args=(concatenated_fields,),
        )
        thread.start()

    def __repr__(self):
        repr = """path:   {path}
{data}""".format(
            path=self.path, data=self.data if self.data is not None else "Empty"
        )
        return repr

    def __del__(self):
        self.flush()

    @property
    def data(self):
        try:
            self.flush()
            if self.path:
                return _safe_open_mfdataset(self.path / "data*.nc")
            return self._concat_fields(self._cached_data)
        except OSError:
            return

    @property
    def metadata(self):
        try:
            if self.path:
                with open(self.path / "metadata.yml", "r") as yaml_file:
                    return yaml.load(yaml_file)
            return self._metadata
        except OSError:
            return

    @metadata.setter
    def metadata(self, parameters):
        if self._mode == "r":
            return
        for key, value in parameters.items():
            self._metadata[key] = value
        if self.path:
            with open(self.path / "metadata.yml", "w") as yaml_file:
                yaml.dump(self._metadata, yaml_file, default_flow_style=False)

    @staticmethod
    def retrieve(path: Path, isel: Union[str, dict, int] = "all", lazy: bool = False):
        """Retrieve the data of a persistent container.

        Parameters
        ----------
        path: Path or str
            The folder where the persistent container lives.
        isel : Union[str, dict, int], optional
            can be either "all" or "last", an integer or a sequence of integer.
            (the default is "all")
        lazy : bool, optional
            if True, return a lazy xarray Datasets that will be loaded when requested
            by the user (using the :py:func:`compute` method). Useful when the data
            are too big to fit in memory. (the default is False)

        Returns
        -------
        :py:class:`FieldsData`
            The requested data, with :py:attr:`FieldsData.data` the fields dataset and
            :py:attr:`FieldsData.metadata` the metadata dictionary.
        """
        path = Path(path)
        if isel == "last":
            last_file = sorted(
                [filename for filename in path.files("data*.nc")],
                key=lambda filename: int(
                    filename.basename().stripext().split("_")[-1].split("-")[-1]
                ),
            )[-1]
            data = _safe_open_dataset(last_file).isel(t=-1)
        else:
            if lazy:
                data = _safe_open_mfdataset(path / "data*.nc", concat_dim="t").sortby(
                    "t"
                )
            else:
                data = concat(
                    [open_dataset(filename) for filename in path.files("data*.nc")],
                    dim="t",
                ).sortby("t")

        with open(Path(path) / "metadata.yml", "r") as yaml_file:
            metadata = yaml.load(yaml_file)

        if isel not in ["all", "last"]:
            data = data.isel(t=isel)

        return FieldsData(data=data, metadata=AttrDict(**metadata))

    def merge(self, override=True):
        if self.path:
            return Container.merge_datafiles(self.path, override=override)

    @staticmethod
    def merge_datafiles(path, override=False):
        path = Path(path)

        if (path / "data.nc").exists() and not override:
            raise FileExistsError(path / "merged_data.nc")
        (path / "data.nc").remove_p()

        split_data = _safe_open_mfdataset(path / "data*.nc", concat_dim="t").sortby("t")
        split_data.to_netcdf(path / "merged_data.nc")
        merged_data = _safe_open_dataset(
            path / "merged_data.nc", chunks=split_data.chunks
        )

        if not split_data.equals(merged_data):
            (path / "merged_data.nc").remove()
            raise IOError("Unable to merge data ")

        split_data.close()
        merged_data.close()

        return path / "merged_data.nc"
