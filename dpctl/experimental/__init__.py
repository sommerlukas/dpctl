#                      Data Parallel Control (dpctl)
#
# Copyright 2020-2024 Intel Corporation
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

"""
    **Data Parallel Control Experimental" provides Python objects to interface
    with different experimental SYCL language extensions defined by the DPC++
    SYCL implementation.

"""
from ._work_group_memory import (
    WorkGroupMemory,
)

from ._raw_kernel_arg import (
    RawKernelArg,
)

__all__ = [
    "WorkGroupMemory",
    "RawKernelArg",
]