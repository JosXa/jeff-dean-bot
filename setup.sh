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
# Run
nohup ./venv/bin/python3 jeffDeanBot.py "207013186:AAHaGrj8R9Ii8rVaUeS0JIWm5aKtY_BTU0U" &>/dev/null 2>&1 &
echo "Bot started and detached."
