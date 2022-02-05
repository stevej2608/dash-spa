#!/bin/bash

# Set up pypicloud. Does nothing if $PYPICLOUD_HOST is not defined

PYPICLOUD_INIT=".devcontainer/pypicloud-init.sh"
chmod +x $PYPICLOUD_INIT && bash $PYPICLOUD_INIT

if [ -f "requirements.txt" ]; then
  python -m pip install --upgrade pip
  pip install pylint
  pip install black
  pip install -r requirements.txt
fi

if [ -f "package.json" ]; then
  npm install
fi
