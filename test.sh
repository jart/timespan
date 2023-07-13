#!/bin/sh
set -ex
python3 setup.py install --prefix ~/.local
python3 timespan/asterisk.py
python3 tests/test.py
