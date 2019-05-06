#!/bin/sh

export FLASK_APP=/www/app.py

if [ -z ${DEBUG+x} ]; then
    export FLASK_DEBUG=0
else
    export FLASK_DEBUG=$DEBUG
fi

python -m flask run --host="0.0.0.0"
