# Add HEC tokens via API calls

This script is intended as an example of how to authenticate in Cribl Stream, and make a simple POST request to add a new HEC token.

Usage:

> py_hec_token_mgr.py [-h] -l http://leader:port [-u USERNAME] -t TOKEN -a {add,modify} [-d DESC] -g GROUP -i INPUT [-p PASSWORD]
* the following arguments are required: -l/--leader, -a/--action, -g/--group, -i/--input
* if no password is supplied, you'll be prompted 
* if you do not specify a token one will be generated for you
* currently the modify action does nothing

Requirements:

* Tested with python 3
* Requires the requests module

# History

* 2022-02-15 - 
  - Moved the leader address to a command line arg

* 2022-02-14
  - initial release

