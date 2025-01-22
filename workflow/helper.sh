#!/bin/bash
set -a # export all vars following, including activation script
A_ENV_LOC="./env"
if [ ! -d "$A_ENV_LOC" ]; then
    # for testing python compatibility
    /opt/homebrew/Cellar/python@3.9/3.9.21/bin/python3.9 -m venv "$A_ENV_LOC"
    #/opt/homebrew/Cellar/python@3.10/3.10.15/bin/python3.10 -m venv "$A_ENV_LOC"
    #/usr/bin/env python3 -m venv "$A_ENV_LOC"
    source "${A_ENV_LOC}/bin/activate"
    pip3 install -r ./requirements.txt
fi
. "${A_ENV_LOC}/bin/activate"
set +a
python ./alfred-linkwarden.py "$@"