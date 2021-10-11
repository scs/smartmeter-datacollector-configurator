#!/usr/bin/env bash

# exit on any error
set -e

# delete previously generated debian directory
rm -rf debian

# copy LICENSE from the root directory
cp ../LICENSE .

# create the debian directory
python setup.py \
    --command-packages=stdeb.command debianize \
    --with-python2=false \
    --with-python3=true \
    --no-python2-scripts=true \
    --with-dh-systemd \
    --compat=10 \
    --build-depends="dh-systemd (>= 1.5)" \
    --recommends3="python3-smartmeter-datacollector"

# remove LICENSE
rm LICENSE

# add Pre-Depends to debian/control for python3-pip
sed -i 's/^\(Depends: \)/Pre-Depends: python3-pip\n\1/' debian/control

# fix the debhelper compatibility level in debian/control
sed -i 's/>= 9/>= 10/' debian/control

PIP_REQUIREMENTS=$(pipenv lock -r)

# write the debian/postinst file
cat <<EOT >> debian/postinst
#!/bin/sh
# postinst script for python3-smartmeter-datacollector-configurator
#
# see: dh_installdeb(1)

# exit on any error
set -e

echo -n "Installing dependencies using pip.."
# write a pip requirements.txt for automatic dependency installation
echo "${PIP_REQUIREMENTS}" > /tmp/requirements.txt
# install all required dependencies
python3 -m pip install -r /tmp/requirements.txt > /dev/null 2>&1
rm /tmp/requirements.txt
echo "..done"

#DEBHELPER#

exit 0
EOT

# copy the systemd unit file to the generated debian directory
SYSTEMD_UNIT_FILE=$(find . -maxdepth 1 -type f -name '*.service' | cut -c 3-)
cp ${SYSTEMD_UNIT_FILE} debian/python3-${SYSTEMD_UNIT_FILE}

echo "SUCCESS: Project has been successfully debianized at debian/"
