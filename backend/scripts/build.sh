#!/usr/bin/env bash

# exit on any error
set -e

CWD=$PWD
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
BACKEND_DIR=${SCRIPT_DIR}/..
ROOT_DIR=${BACKEND_DIR}/..
FRONTEND_DIR=${ROOT_DIR}/frontend/smartmeter-datacollector-configurator

BACKEND_STATIC_DIR=${BACKEND_DIR}/smartmeter_datacollector_configurator/static
FRONTEND_DIST_DIR=${FRONTEND_DIR}/dist

# Delete previously built distribution
rm -rf ${BACKEND_DIR}/build ${BACKEND_DIR}/dist ${BACKEND_STATIC_DIR} ${FRONTEND_DIST_DIR}

# fail if setup.py is not up-to-date
echo -n "Checking whether Pipfile and setup.py are synchronized..."
pipenv-setup check > /dev/null 2>&1 || {
    echo "FAILED"
    echo ""
    echo "Pipfile and setup.py are out of sync!"
    echo "Run \"pipenv run setup\" to fix this."
    exit 1
}
echo "OK"
echo ""

# build the frontend
echo "Building the frontend for distribution..."
cd ${FRONTEND_DIR}
npm run build

# copy the built frontend to the static directory
mkdir -p ${BACKEND_STATIC_DIR}
cp -R ${FRONTEND_DIST_DIR}/* ${BACKEND_STATIC_DIR}/

# copy LICENSE and README.md from the root directory
cp ${ROOT_DIR}/{LICENSE,README.md} ${BACKEND_DIR}

cd ${BACKEND_DIR}

# build the source distribution and binary distribution wheel
echo "Building the Python package..."
python setup.py -q sdist bdist_wheel

# remove LICENSE and README.md
rm ${BACKEND_DIR}/{LICENSE,README.md}

echo "SUCCESS: Packages have been successfully built at dist/"
