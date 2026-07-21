#!/bin/sh
PORT=${PORT:-5000}
gunicorn --bind 0.0.0.0:$PORT manage:app