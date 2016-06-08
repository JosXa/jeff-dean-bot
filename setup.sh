#!/bin/bash
export WORKSPACE=`pwd`
# Create/Activate virtualenv
virtualenv venv
source venv/bin/activate
# Install Requirements
pip3 install -r requirements.txt
