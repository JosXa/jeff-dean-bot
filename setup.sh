#!/bin/bash
# Kill all
echo "Killing all previous instances..."
ps -ef | grep jeffDeanBot.py | grep -v grep | awk '{print $2}' | xargs -r kill -9
export WORKSPACE=`pwd`
# Create/Activate virtualenv
virtualenv venv
source "$WORKSPACE/venv/bin/activate"
# Install Requirements
pip3 install -r requirements.txt

