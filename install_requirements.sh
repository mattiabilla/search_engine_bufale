#!/bin/sh
python3 -m pip install -r requirements.txt 
cd server
export FLASK_APP=server