#!/bin/bash

# Virtual Env Stuff
python3 -m venv myenv
source ./myenv/bin/activate
pip install -r requirements.txt

echo -e "*****************************************************************"

echo -e "************ ENVIRONMENT SETUP COMPLETE! Run: flask run **********"

echo -e "*****************************************************************"
