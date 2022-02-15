# Add HEC tokens via API calls

This script is intended as an example of how to authenticate, and make a simple POST request to add a new HEC token.

Usage:

> py_hec_token_mgr.py [-h] [-u USERNAME] -t TOKEN -a {add,modify} [-d DESC] -g GROUP -i INPUT [-p PASSWORD]
* the following arguments are required: -t/--token, -a/--action, -g/--group, -i/--input
* if no password is supplied, you'll be prompted 
* currently the modify action does nothing

Requirements:

* Tested with python 3
* Requires the requests module
* You'll need to edit the script to include your leader node hostname or IP


