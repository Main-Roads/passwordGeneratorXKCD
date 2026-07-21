#!/bin/sh
PORT=${PORT:-5000}
wget -q -O - http://127.0.0.1:$PORT/version > /dev/null || exit 1