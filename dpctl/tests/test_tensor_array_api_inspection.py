#                      Data Parallel Control (dpctl)
#
# Copyright 2020-2025 Intel Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pytest

import dpctl
import dpctl.tensor as dpt
from dpctl.tensor._tensor_impl import (
    default_device_complex_type,
    default_device_fp_type,
    default_device_index_type,
    default_device_int_type,
)

_dtypes_no_fp16_fp64 = {
    "bool": dpt.bool,
    "float32": dpt.float32,
    "complex64": dpt.complex64,
    "int8": dpt.int8,
    "int16": dpt.int16,
    "int32": dpt.int32,
    "int64": dpt.int64,
    "uint8": dpt.uint8,
    "uint16": dpt.uint16,
    "uint32": dpt.uint32,
    "uint64": dpt.uint64,
}


def test_array_api_inspection_methods():
    info = dpt.__array_namespace_info__()
    assert info.capabilities()
    try:
        assert info.default_device()
    except dpctl.SyclDeviceCreationError:
        pytest.skip("No default device available")
    assert info.default_dtypes()
    assert info.devices()
    assert info.dtypes()


def test_array_api_inspection_default_device():
    try:
        dev = dpctl.select_default_device()
    except dpctl.SyclDeviceCreationError:
        pytest.skip("No default device available")
    assert dpt.__array_namespace_info__().default_device() == dev


def test_array_api_inspection_devices():
    try:
        devices2 = dpctl.get_devices()
    except dpctl.SyclDeviceCreationError:
        pytest.skip("No default device available")
    devices1 = dpt.__array_namespace_info__().devices()
    assert len(devices1) == len(devices2)
    assert devices1 == devices2


def test_array_api_inspection_capabilities():
    capabilities = dpt.__array_namespace_info__().capabilities()
    assert capabilities["boolean indexing"]
    assert capabilities["data-dependent shapes"]
    assert capabilities["max dimensions"] is None


def test_array_api_inspection_default_dtypes():
    try:
        dev = dpctl.select_default_device()
    except dpctl.SyclDeviceCreationError:
        pytest.skip("No default device available")

    int_dt = default_device_int_type(dev)
    ind_dt = default_device_index_type(dev)
    fp_dt = default_device_fp_type(dev)
    cm_dt = default_device_complex_type(dev)

    info = dpt.__array_namespace_info__()
    default_dts_nodev = info.default_dtypes()
    default_dts_dev = info.default_dtypes(device=dev)

    assert (
        int_dt == default_dts_nodev["integral"] == default_dts_dev["integral"]
    )
    assert (
        ind_dt == default_dts_nodev["indexing"] == default_dts_dev["indexing"]
    )
    assert (
        fp_dt
        == default_dts_nodev["real floating"]
        == default_dts_dev["real floating"]
    )
    assert (
        cm_dt
        == default_dts_nodev["complex floating"]
        == default_dts_dev["complex floating"]
    )


def test_array_api_inspection_default_device_dtypes():
    try:
        dev = dpctl.select_default_device()
    except dpctl.SyclDeviceCreationError:
        pytest.skip("No default device available")
    dtypes = _dtypes_no_fp16_fp64.copy()
    if dev.has_aspect_fp64:
        dtypes["float64"] = dpt.float64
        dtypes["complex128"] = dpt.complex128

    assert dtypes == dpt.__array_namespace_info__().dtypes()


def test_array_api_inspection_device_dtypes():
    info = dpt.__array_namespace_info__()
    try:
        dev = info.default_device()
    except dpctl.SyclDeviceCreationError:
        pytest.skip("No default device available")
    dtypes = _dtypes_no_fp16_fp64.copy()
    if dev.has_aspect_fp64:
        dtypes["float64"] = dpt.float64
        dtypes["complex128"] = dpt.complex128

    assert dtypes == dpt.__array_namespace_info__().dtypes(device=dev)


def test_array_api_inspection_dtype_kind():
    info = dpt.__array_namespace_info__()
    try:
        info.default_device()
    except dpctl.SyclDeviceCreationError:
        pytest.skip("No default device available")

    f_dtypes = info.dtypes(kind="real floating")
    assert all([_dt[1].kind == "f" for _dt in f_dtypes.items()])

    i_dtypes = info.dtypes(kind="signed integer")
    assert all([_dt[1].kind == "i" for _dt in i_dtypes.items()])

    u_dtypes = info.dtypes(kind="unsigned integer")
    assert all([_dt[1].kind == "u" for _dt in u_dtypes.items()])

    ui_dtypes = info.dtypes(kind="unsigned integer")
    assert all([_dt[1].kind in "ui" for _dt in ui_dtypes.items()])

    c_dtypes = info.dtypes(kind="complex floating")
    assert all([_dt[1].kind == "c" for _dt in c_dtypes.items()])

    assert info.dtypes(kind="bool") == {"bool": dpt.bool}

    _signed_ints = {
        "int8": dpt.int8,
        "int16": dpt.int16,
        "int32": dpt.int32,
        "int64": dpt.int64,
    }
    assert (
        info.dtypes(kind=("signed integer", "signed integer")) == _signed_ints
    )
    assert (
        info.dtypes(
            kind=("integral", "bool", "real floating", "complex floating")
        )
        == info.dtypes()
    )
    assert info.dtypes(
        kind=("integral", "real floating", "complex floating")
    ) == info.dtypes(kind="numeric")


def test_array_api_inspection_dtype_kind_errors():
    info = dpt.__array_namespace_info__()
    try:
        info.default_device()
    except dpctl.SyclDeviceCreationError:
        pytest.skip("No default device available")

    with pytest.raises(ValueError):
        info.dtypes(kind="error")

    with pytest.raises(TypeError):
        info.dtypes(kind={0: "real floating"})


def test_array_api_inspection_device_types():
    info = dpt.__array_namespace_info__()
    try:
        dev = info.default_device()
    except dpctl.SyclDeviceCreationError:
        pytest.skip("No default device available")

    q = dpctl.SyclQueue(dev)
    assert info.default_dtypes(device=q)
    assert info.dtypes(device=q)

    dev_dpt = dpt.Device.create_device(dev)
    assert info.default_dtypes(device=dev_dpt)
    assert info.dtypes(device=dev_dpt)

    filter = dev.get_filter_string()
    assert info.default_dtypes(device=filter)
    assert info.dtypes(device=filter)


def test_array_api_inspection_device_errors():
    info = dpt.__array_namespace_info__()

    bad_dev = dict()
    with pytest.raises(TypeError):
        info.dtypes(device=bad_dev)

    with pytest.raises(TypeError):
        info.default_dtypes(device=bad_dev)
