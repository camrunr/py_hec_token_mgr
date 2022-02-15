#!/usr/bin/python

import requests
import json
import os
import sys
import argparse
import getpass

# where we login to get a bearer token
auth_uri = '/api/v1/auth/login'
# where we post to add a token (GROUP and INPUT will be replaced from args)
add_uri  = '/api/v1/m/GROUP/system/inputs/INPUT/hectoken'

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
    parser.add_argument('-l', '--leader', help='Specify leader URL, http(s)://leader:port',required=True)
    parser.add_argument('-u', '--username', help='Specify username, or default is admin',default='admin')
    parser.add_argument('-t', '--token', type=str, help="The target HEC token", required=True)
    parser.add_argument('-a', '--action', type=str, help="The action: add or modify", choices=['add','modify'], required=True)
    parser.add_argument('-d', '--desc', type=str, help="The token descriptor, defaults to empty",default="")
    parser.add_argument('-g', '--group', type=str, help="The target worker group", required=True)
    parser.add_argument('-i', '--input', type=str, help="The target inputId", required=True) 
    parser.add_argument('-p', '--password', type=Password, help='Specify password, or get prompted',default=Password.DEFAULT)
    args = parser.parse_args()
    return args

def auth(leader_url,un,pw):
    # get logged in and grab a token
    header = {'accept': 'application/json', 'Content-Type': 'application/json'}
    login = '{"username": "' + un + '", "password": "' + pw + '"}'
    r = requests.post(leader_url+auth_uri,headers=header,data=login,verify=False)
    if (r.status_code == 200):
        res = r.json()
        return res["token"]
    else:
        print("Login failed, terminating")
        print(str(r.json()))
        sys.exit()

def add_token(header, args):
    # send the request to create the token
    jd = {"description": args.desc, "token": args.token }
    my_uri = add_uri.replace('GROUP', args.group).replace('INPUT',args.input)
    r = requests.post(args.leader+my_uri,headers=header,json=jd,verify=False)
    if r.status_code == 200:
        print("good!")
        return True
    else:
        print(r.status_code)
        print("bad! Response JSON follows:\n" + str(r.json()))
        return False

def mod_token(header,args):
    # not implemented yet
    return True

if __name__ == "__main__":
    args = parse_args()
    bearer_token = auth(args.leader,args.username, str(args.password))
    header = { 'accept': 'application/json', 'Content-Type': 'application/json', 'Authorization': 'Bearer ' + bearer_token }
    #print(bearer_token)
    add_token(header,args)