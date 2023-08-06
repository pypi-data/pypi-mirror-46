#
# Copyright 2017-2019 European Centre for Medium-Range Weather Forecasts (ECMWF).
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Authors:
#   Alessandro Amici - B-Open - https://bopen.eu
#

import logging
import typing as T  # noqa
import warnings

import xarray as xr

from . import DatasetBuildError

LOGGER = logging.getLogger(__name__)


def open_dataset(path, **kwargs):
    # type: (str, T.Any) -> xr.Dataset
    """
    Return a ``xr.Dataset`` with the requested ``backend_kwargs`` from a GRIB file.
    """
    if 'engine' in kwargs and kwargs['engine'] != 'cfgrib':
        raise ValueError("only engine=='cfgrib' is supported")
    kwargs['engine'] = 'cfgrib'
    return xr.backends.api.open_dataset(path, **kwargs)


def open_datasets(path, backend_kwargs={}, no_warn=False, **kwargs):
    # type: (str, T.Dict[str, T.Any], bool, T.Any) -> T.List[xr.Dataset]
    """
    Open a GRIB file groupping incompatible hypercubes to different datasets via simple heuristics.
    """
    if not no_warn:
        warnings.warn("open_datasets is an experimental API, DO NOT RELY ON IT!", FutureWarning)

    fbks = []
    datasets = []
    try:
        datasets.append(open_dataset(path, backend_kwargs=backend_kwargs, **kwargs))
    except DatasetBuildError as ex:
        fbks.extend(ex.args[2])
    # NOTE: the recursive call needs to stay out of the exception handler to avoid showing
    #   to the user a confusing error message due to exception chaining
    for fbk in fbks:
        bks = backend_kwargs.copy()
        bks['filter_by_keys'] = fbk
        datasets.extend(open_datasets(path, backend_kwargs=bks, no_warn=True, **kwargs))
    return datasets
