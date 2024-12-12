//===---- dpctl_sycl_extension_interface.cpp - Implements C API for SYCL ext =//
//
//                      Data Parallel Control (dpctl)
//
// Copyright 2020-2024 Intel Corporation
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//    http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.
//
//===----------------------------------------------------------------------===//
///
/// \file
/// This file implements the data types and functions declared in
/// dpctl_sycl_extension_interface.h.
///
//===----------------------------------------------------------------------===//

#include "dpctl_sycl_extension_interface.h"

#include "dpctl_error_handlers.h"
#include "dpctl_sycl_type_casters.hpp"

#include <sycl/sycl.hpp>

using namespace sycl;

namespace syclext = sycl::ext::oneapi::experimental;

using namespace dpctl::syclinterface;

DPCTL_API
__dpctl_give DPCTLSyclRawKernelArgRef DPCTLRawKernelArg_Create(size_t count,
                                                               void *bytes)
{
    DPCTLSyclRawKernelArgRef ka = nullptr;

    try {
        auto ptr = static_cast<uint32_t*>(bytes);
        std::cout << ptr[0] << ", " << ptr[1] << std::endl;
        auto RawArg = new syclext::raw_kernel_arg(bytes, count);
        ka = wrap<syclext::raw_kernel_arg>(RawArg);
    } catch (std::exception const &e) {
        error_handler(e, __FILE__, __func__, __LINE__);
    }

    return ka;
}

DPCTL_API
void DPCTLRawKernelArg_Delete(__dpctl_take DPCTLSyclRawKernelArgRef Ref)
{
    delete unwrap<syclext::raw_kernel_arg>(Ref);
}
