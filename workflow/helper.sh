#!/bin/bash
set -a # export all vars following, including activation script
ENV_LOC="./env"
if [ ! -d "$ENV_LOC" ]; then 
    /usr/bin/env python3 -m venv "$ENV_LOC"
    source "${ENV_LOC}/bin/activate"
    pip3 install -r ./requirements.txt
fi
. "${ENV_LOC}/bin/activate"
set +a
python ./alfred-linkwarden.py "$@"