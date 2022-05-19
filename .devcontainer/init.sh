#!/bin/bash

if [ -f "requirements.txt" ]; then
  python -m pip install --upgrade pip
  pip install pylint
  pip install black
  pip install -r requirements.txt
fi

if [ -f "package.json" ]; then
  npm install
fi
