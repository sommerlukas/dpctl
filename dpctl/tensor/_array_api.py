#                       Data Parallel Control (dpctl)
#
#  Copyright 2020-2025 Intel Corporation
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import dpctl
import dpctl.tensor as dpt
from dpctl.tensor._tensor_impl import (
    default_device_complex_type,
    default_device_fp_type,
    default_device_index_type,
    default_device_int_type,
)


def _isdtype_impl(dtype, kind):
    if isinstance(kind, str):
        if kind == "bool":
            return dtype.kind == "b"
        elif kind == "signed integer":
            return dtype.kind == "i"
        elif kind == "unsigned integer":
            return dtype.kind == "u"
        elif kind == "integral":
            return dtype.kind in "iu"
        elif kind == "real floating":
            return dtype.kind == "f"
        elif kind == "complex floating":
            return dtype.kind == "c"
        elif kind == "numeric":
            return dtype.kind in "iufc"
        else:
            raise ValueError(f"Unrecognized data type kind: {kind}")

    elif isinstance(kind, tuple):
        return any(_isdtype_impl(dtype, k) for k in kind)
    else:
        raise TypeError(f"Unsupported type for dtype kind: {type(kind)}")


def _get_device_impl(d):
    if d is None:
        return dpctl.select_default_device()
    elif isinstance(d, dpctl.SyclDevice):
        return d
    elif isinstance(d, (dpt.Device, dpctl.SyclQueue)):
        return d.sycl_device
    else:
        try:
            return dpctl.SyclDevice(d)
        except TypeError:
            raise TypeError(f"Unsupported type for device argument: {type(d)}")


__array_api_version__ = "2024.12"


class Info:
    """
    namespace returned by ``__array_namespace_info__()``
    """

    def __init__(self):
        self._capabilities = {
            "boolean indexing": True,
            "data-dependent shapes": True,
            "max dimensions": None,
        }
        self._all_dtypes = {
            "bool": dpt.bool,
            "float32": dpt.float32,
            "float64": dpt.float64,
            "complex64": dpt.complex64,
            "complex128": dpt.complex128,
            "int8": dpt.int8,
            "int16": dpt.int16,
            "int32": dpt.int32,
            "int64": dpt.int64,
            "uint8": dpt.uint8,
            "uint16": dpt.uint16,
            "uint32": dpt.uint32,
            "uint64": dpt.uint64,
        }

    def capabilities(self):
        """
        capabilities()

        Returns a dictionary of ``dpctl``'s capabilities.

        The dictionary contains the following keys:
            ``"boolean indexing"``:
                boolean indicating ``dpctl``'s support of boolean indexing.
                Value: ``True``
            ``"data-dependent shapes"``:
                boolean indicating ``dpctl``'s support of data-dependent shapes.
                Value: ``True``
            ``max dimensions``:
                integer indication the maximum array dimension supported by ``dpctl``.
                Value: ``None``

        Returns:
            dict:
                dictionary of ``dpctl``'s capabilities
        """
        return self._capabilities.copy()

    def default_device(self):
        """
        default_device()

        Returns the default SYCL device.
        """
        return dpctl.select_default_device()

    def default_dtypes(self, *, device=None):
        """
        default_dtypes(*, device=None)

        Returns a dictionary of default data types for ``device``.

        Args:
            device (Optional[:class:`dpctl.SyclDevice`, :class:`dpctl.SyclQueue`, :class:`dpctl.tensor.Device`, str]):
                array API concept of device used in getting default data types.
                ``device`` can be ``None`` (in which case the default device
                is used), an instance of :class:`dpctl.SyclDevice`, an instance
                of :class:`dpctl.SyclQueue`, a :class:`dpctl.tensor.Device`
                object returned by :attr:`dpctl.tensor.usm_ndarray.device`, or
                a filter selector string.
                Default: ``None``.

        Returns:
            dict:
                a dictionary of default data types for ``device``:

                    - ``"real floating"``: dtype
                    - ``"complex floating"``: dtype
                    - ``"integral"``: dtype
                    - ``"indexing"``: dtype
        """
        device = _get_device_impl(device)
        return {
            "real floating": dpt.dtype(default_device_fp_type(device)),
            "complex floating": dpt.dtype(default_device_complex_type(device)),
            "integral": dpt.dtype(default_device_int_type(device)),
            "indexing": dpt.dtype(default_device_index_type(device)),
        }

    def dtypes(self, *, device=None, kind=None):
        """
        dtypes(*, device=None, kind=None)

        Returns a dictionary of all Array API data types of a specified
        ``kind`` supported by ``device``.

        This dictionary only includes data types supported by the
        `Python Array API <https://data-apis.org/array-api/latest/>`_
        specification.

        Args:
            device (Optional[:class:`dpctl.SyclDevice`, :class:`dpctl.SyclQueue`, :class:`dpctl.tensor.Device`, str]):
                array API concept of device used in getting default data types.
                ``device`` can be ``None`` (in which case the default device is
                used), an instance of :class:`dpctl.SyclDevice`, an instance of
                :class:`dpctl.SyclQueue`, a :class:`dpctl.tensor.Device`
                object returned by :attr:`dpctl.tensor.usm_ndarray.device`, or
                a filter selector string.
                Default: ``None``.

            kind (Optional[str, Tuple[str, ...]]):
                data type kind.

                - if ``kind`` is ``None``, returns a dictionary of all data
                  types supported by `device`
                - if ``kind`` is a string, returns a dictionary containing the
                  data types belonging to the data type kind specified.

                  Supports:

                  * ``"bool"``
                  * ``"signed integer"``
                  * ``"unsigned integer"``
                  * ``"integral"``
                  * ``"real floating"``
                  * ``"complex floating"``
                  * ``"numeric"``

                - if ``kind`` is a tuple, the tuple represents a union of
                  ``kind`` strings, and returns a dictionary containing data
                  types corresponding to the-specified union.

                Default: ``None``.

        Returns:
            dict:
                a dictionary of the supported data types of the specified
                ``kind``
        """
        device = _get_device_impl(device)
        _fp64 = device.has_aspect_fp64
        if kind is None:
            return {
                key: val
                for key, val in self._all_dtypes.items()
                if _fp64 or (key != "float64" and key != "complex128")
            }
        else:
            return {
                key: val
                for key, val in self._all_dtypes.items()
                if (_fp64 or (key != "float64" and key != "complex128"))
                and _isdtype_impl(val, kind)
            }

    def devices(self):
        """
        devices()

        Returns a list of supported devices.
        """
        return dpctl.get_devices()


def __array_namespace_info__():
    """
    __array_namespace_info__()

    Returns a namespace with Array API namespace inspection utilities.

    """
    return Info()
