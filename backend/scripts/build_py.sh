#!/usr/bin/env bash

# exit on any error
set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

BACKEND_DIR=${SCRIPT_DIR}/..
BACKEND_DIST_DIR="${BACKEND_DIR}/dist"
ROOT_DIR=${BACKEND_DIR}/..
FRONTEND_DIR=${ROOT_DIR}/frontend/smartmeter-datacollector-configurator
FRONTEND_DIST_DIR=${FRONTEND_DIR}/dist
BACKEND_STATIC_DIR=${BACKEND_DIR}/smartmeter_datacollector_configurator/static

# delete previously built artifacts
echo -n "Cleaning up from previous builds.."
rm -rf "${BACKEND_DIST_DIR}" "${BACKEND_STATIC_DIR}" "${FRONTEND_DIST_DIR}"
echo "..done"

# build the frontend
(
    cd "${FRONTEND_DIR}"
    echo "Building the frontend for distribution..."
    npm run build
    echo "..done"
)

# copy the built frontend to the static directory
mkdir -p "${BACKEND_STATIC_DIR}"
cp -R "${FRONTEND_DIST_DIR}/"* "${BACKEND_STATIC_DIR}/"
cp "${ROOT_DIR}/LICENSE" "${BACKEND_DIR}"

# build the Python package
echo "Building Python source package.."
poetry build --format=sdist --output="${BACKEND_DIST_DIR}"
echo "..done"

echo "Building Python wheel.."
poetry build --format=wheel --output="${BACKEND_DIST_DIR}"
echo "..done"

# clean up
rm -rf "${BACKEND_DIR}/LICENSE" "${BACKEND_STATIC_DIR}"

echo "SUCCESS: Python source package and wheel have been successfully built at '${BACKEND_DIST_DIR}/'"
