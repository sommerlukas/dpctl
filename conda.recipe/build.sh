#!/bin/bash

# We need dpcpp to compile dppy_oneapi_interface
if [ ! -z "${ONEAPI_ROOT}" ]; then
    if [ -f "${ONEAPI_ROOT}/compiler/latest/env/vars.no_fpga.sh" ]; then
        source ${ONEAPI_ROOT}/compiler/latest/env/vars.no_fpga.sh
    else
        source ${ONEAPI_ROOT}/compiler/latest/env/vars.sh
    fi
    export CC=clang
    export CXX=dpcpp
else
    echo "DPCPP is needed to build DPPY. Abort!"
    exit 1
fi

rm -rf build
mkdir build
cd build

cmake                                    \
    -DCMAKE_BUILD_TYPE=Release           \
    -DCMAKE_INSTALL_PREFIX=${PREFIX}     \
    -DCMAKE_PREFIX_PATH=${PREFIX}        \
    ..

make -j 4 && make install

cd ../python_binding

# required by dpglue
export DP_GLUE_LIBDIR=${PREFIX}
export DP_GLUE_INCLDIR=${PREFIX}/include
export OpenCL_LIBDIR=${ONEAPI_ROOT}/compiler/latest/linux/lib
# required by oneapi_interface
export DPPY_ONEAPI_INTERFACE_LIBDIR=${INSTALL_PREFIX}/lib
export DPPY_ONEAPI_INTERFACE_INCLDIR=${INSTALL_PREFIX}/include

# FIXME: How to pass this using setup.py? This flags is needed when
# dpcpp compiles the generated cpp file.
export CFLAGS="-fPIC -O3 ${CFLAGS}"
export LDFLAGS="-L OpenCL_LIBDIR ${LDFLAGS}"
${PYTHON} setup.py clean --all
${PYTHON} setup.py build
${PYTHON} setup.py install