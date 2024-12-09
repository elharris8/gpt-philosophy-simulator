#!/bin/bash

# Virtual Env Stuff
python -m venv myenv
source myenv/bin/activate

pip install -r requirements.txt

export FLASK_APP=app
export FLASK_ENV=development
export FLASK_DEBUG=1


echo -e "*****************************************************************"

echo -e "************ ENVIRONMENT SETUP COMPLETE! Run: flask run**********"

echo -e "*****************************************************************"
