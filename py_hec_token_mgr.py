#!/usr/bin/python

import requests
import json
import os
import sys
import argparse
import getpass
import secrets
import argparse

requests.urllib3.disable_warnings(requests.urllib3.exceptions.InsecureRequestWarning)
# where we login to get a bearer token
auth_uri = '/api/v1/auth/login'
# where we post to add a token (GROUP and INPUT will be replaced from args)
add_uri  = '/api/v1/m/GROUP/system/inputs/INPUT/hectoken'

# create a keyvalue class
class keyvalue(argparse.Action):
    # Constructor calling
    def __call__( self , parser, namespace,
                 values, option_string = None):
        setattr(namespace, self.dest, dict())
          
        for value in values:
            # split it into key and value
            key, value = value.split('=')
            # assign into dictionary
            getattr(namespace, self.dest)[key] = value

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
    parser.add_argument('-t', '--token', type=str, help="Specify your own token, if you don't want one generated.", default='')
    parser.add_argument('-a', '--action', type=str, help="The action: add or modify", choices=['add','modify'], required=True)
    parser.add_argument('-d', '--desc', type=str, help="The token descriptor, defaults to empty",default="")
    parser.add_argument('-g', '--group', type=str, help="The target worker group", required=True)
    parser.add_argument('-i', '--input', type=str, help="The target inputId", required=True) 
    parser.add_argument('-p', '--password', type=Password, help='Specify password, or get prompted',default=Password.DEFAULT)
    parser.add_argument('-m', '--metadata', nargs='*', help='Pass metadata to the script in key:value pair form. Javascript expression allowed. Multiple fields allowed ex: -m index=\"\'test\'\" sourcetype=\"\'mysource\'\"' , action = keyvalue, default='')
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
    if not args.metadata:
        jd = {"description": args.desc, "token": args.token }
        my_uri = add_uri.replace('GROUP', args.group).replace('INPUT',args.input)
        r = requests.post(args.leader+my_uri,headers=header,json=jd,verify=False)
        if r.status_code == 200:
            print("good!")
            print("Generated Token is: " + args.token)
            return True
        else:
            print(r.status_code)
            print("bad! Response JSON follows:\n" + str(r.json()))
            return False
    else:
        metadata=get_metadata()
        jd = {"description": args.desc, "token": args.token, "metadata": metadata }
        my_uri = add_uri.replace('GROUP', args.group).replace('INPUT',args.input)
        r = requests.post(args.leader+my_uri,headers=header,json=jd,verify=False)
        if r.status_code == 200:
            print("Success!")
            print("Generated Token is: " + args.token)
            return True
        else:
            print(r.status_code)
            print("Failed! Response JSON follows:\n" + str(r.json()))
            return False
    

def get_metadata():
    metadata=args.metadata
    #print(metadata)
    meta_json = []
    for k, v in metadata.items():
        meta_json.append({'name': k, 'value': v})
    return meta_json

def mod_token(header,args):
    mod_uri  = '/api/v1/m/GROUP/system/inputs/INPUT/hectoken/'+args.token
    metadata=get_metadata()
    #print(metadata)
    jd = {"description": args.desc, "token": args.token, "metadata": metadata }
    my_uri = mod_uri.replace('GROUP', args.group).replace('INPUT',args.input)
    r = requests.patch(args.leader+my_uri,headers=header,json=jd,verify=False)
    if r.status_code == 200:
        print("Sucessfully updated token: " + args.token)
        return True
    else:
        print(r.status_code)
        print("Error: Response JSON follows:\n" + str(r.json()))
        return False

def build_token():
    hec_token=secrets.token_hex(4) + "-" + secrets.token_hex(2) + "-" + secrets.token_hex(2) + "-" + secrets.token_hex(2)+ "-" + secrets.token_hex(6)
    return hec_token

if __name__ == "__main__":
    args = parse_args()
    if args.action == 'add':
        if not args.token:
            args.token=build_token()
        else:
            args.token=args.token
        bearer_token = auth(args.leader,args.username, str(args.password))
        header = { 'accept': 'application/json', 'Content-Type': 'application/json', 'Authorization': 'Bearer ' + bearer_token }
        #print(bearer_token)
        add_token(header,args)
    else:
        print("modify")
        bearer_token = auth(args.leader,args.username, str(args.password))
        header = { 'accept': 'application/json', 'Content-Type': 'application/json', 'Authorization': 'Bearer ' + bearer_token }
        #print(bearer_token)
        mod_token(header,args)