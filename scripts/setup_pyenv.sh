#!/usr/bin/env bash
set -e

PYTHON_VERSION=$1

if [ -z "$PYTHON_VERSION" ]; then
    echo "usage: setup-pyenv.sh <python_version>"
    exit 1
fi

venv_name=$(poetry env info -p | sed 's/.*\///')
if [ ! -z "$venv_name" ]; then
    echo "$venv_name"
    poetry env remove "$venv_name"
fi

pyenv local "$PYTHON_VERSION"
poetry env use "$PYTHON_VERSION"
