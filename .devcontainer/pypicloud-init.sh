#!/bin/bash
#
# Settings needed to upload and download python packages from a local
# pypicloud repo.

if [[ -z "$PYPICLOUD_HOST" ]]; then
    exit 0
fi

echo "*** Configuring pypi ***"

# Needed to upload packages - twine upload -r pypicloud dist/*

cat > ~/.pypirc <<EOF
[distutils]
index-servers =
  pypicloud

[pypicloud]
repository: http://$PYPICLOUD_HOST:6543/simple/
username: $PYPICLOUD_USER
password: $PYPICLOUD_PASSWORD
EOF

# Needed to download packages - pip install ...
#
# https://pypicloud.readthedocs.io/en/latest/topics/getting_started.html

PIP_CONF=~/.pip/pip.conf

mkdir -p "$(dirname "$PIP_CONF")" && touch "$PIP_CONF"

cat > $PIP_CONF <<EOF
[global]
index-url = http://$PYPICLOUD_HOST:6543/simple/
trusted-host = $PYPICLOUD_HOST
EOF

