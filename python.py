#!//usr/bin/python

import requests
import json
import os
import sys
import argparse
from getpass import getpass

class Password:

    DEFAULT = 'Prompt if not specified'

    def __init__(self, value):
        if value == self.DEFAULT:
            value = getpass.getpass('Password: ')
        self.value = value

    def __str__(self):
        return self.value

def main():
    url = 'http://192.168.100.111:9000/api/v1/auth/login'

    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-u', '--username', help='Specify username',
        default=getpass.getuser())
    parser.add_argument('-p', '--password', type=Password, help='Specify password',
        default=Password.DEFAULT)
    args = parser.parse_args()

    print(args.username, args.password)


    # get logged in and grab a token
    header = {'accept': 'application/json', 'Content-Type': 'application/json'}
    login = '{"username": "' + args.username + '", "password": "' + args.password + '"}'
    r = requests.post(url,headers=header,data=login,verify=False)
    res = r.json()
    bearerToken=res["token"]
    print(bearerToken)

if __name__ == "__main__":
    main()