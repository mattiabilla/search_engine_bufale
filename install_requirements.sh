#!/bin/sh
python3 -m pip3 install -r requirements.txt 
cd server
export FLASK_APP=server