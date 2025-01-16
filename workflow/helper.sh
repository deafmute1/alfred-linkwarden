#!/bin/bash
set -a # export all vars following, including activation script
A_ENV_LOC="./env"
if [ ! -d "$A_ENV_LOC" ]; then 
    /usr/bin/env python3 -m venv "$A_ENV_LOC"
    source "${A_ENV_LOC}/bin/activate"
    pip3 install -r ./requirements.txt
fi
. "${A_ENV_LOC}/bin/activate"
set +a
python ./alfred-linkwarden.py "$@"