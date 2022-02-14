#!/usr/bin/python

import requests
import json
import os
import sys
import argparse
import getpass

api_base = 'http://192.168.100.111:9000'
auth_uri = '/api/v1/auth/login'
add_uri = '/api/v1/m/GROUP/system/inputs/INPUT/hectoken'


class Password:
    # if password is provided, use it. otherwise prompt
    DEFAULT = 'Prompt if not specified'

    def __init__(self, value):
        if value == self.DEFAULT:
            value = getpass.getpass('Password: ')
        self.value = value

    def __str__(self):
        return self.value

def parse_args():
    # parse the command args
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-u', '--username', help='Specify username, or default is admin',default='admin')
    parser.add_argument('-t', '--token', type=str, help="The target HEC token", required=True)
    parser.add_argument('-a', '--action', type=str, help="The action: add or modify", choices=['add','modify'], required=True)
    parser.add_argument('-d', '--desc', type=str, help="The token descriptor, defaults to empty",default="")
    parser.add_argument('-g', '--group', type=str, help="The target worker group", required=True)
    parser.add_argument('-i', '--input', type=str, help="The target inputId", required=True) 
    parser.add_argument('-p', '--password', type=Password, help='Specify password, or get prompted',default=Password.DEFAULT)
    args = parser.parse_args()
    return args

def auth(un,pw):
    # get logged in and grab a token
    header = {'accept': 'application/json', 'Content-Type': 'application/json'}
    login = '{"username": "' + un + '", "password": "' + pw + '"}'
    r = requests.post(api_base+auth_uri,headers=header,data=login,verify=False)
    res = r.json()
    return res["token"]


    #header = {'Authorization': 'Bearer {}'.format(bearer_token)}
def add_token(bt, args):
    header = { 'accept': 'application/json', 'Content-Type': 'application/json', 'Authorization': 'Bearer ' + bt }
    #d = { 'description': args.desc, 'token': args.token, "metadata": [{"test": "value"}] }
    da = { 'description': args.desc, 'token': args.token }
    fixed_uri = add_uri.replace('GROUP', args.group).replace('INPUT',args.input)
    r = requests.post(api_base+fixed_uri,headers=header,data=da,verify=False)
    if r.status_code == "200":
        print("good!")
        return True
    else:
        print("bad! JSON follows:\n")
        print(r.json())
        return False

def mod_token(bt,args):
    header = { 'accept': 'application/json', 'Content-Type': 'application/json', 'Authorization': 'Bearer ' + bt }
    # not implemented yet

if __name__ == "__main__":
    args = parse_args()
    bearer_token = auth(args.username, str(args.password))
    print(bearer_token)
    add_token(bearer_token,args)