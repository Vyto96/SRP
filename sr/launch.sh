#!/bin/bash
export FLASK_APP=sr

gunicorn -b "127.0.0.1:4000" sr:app -w 4 &
