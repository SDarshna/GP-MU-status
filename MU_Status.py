#!/usr/bin/env python3

import prisma_sase
import io
import requests
import json
import os
import termtables as tt
import yaml
import argparse


def sdk_login_to_controller(filepath):
    with open(filepath) as f:
        client_secret_dict = yaml.safe_load(f)
        client_id = client_secret_dict["client_id"]
        client_secret = client_secret_dict["client_secret"]
        tsg_id_str = client_secret_dict["scope"]
        global tsg
        tsg = tsg_id_str.split(":")[1]
        #print(client_id, client_secret, tsg)

    global sdk 
    sdk = prisma_sase.API(controller="https://sase.paloaltonetworks.com/", ssl_verify=False)
   
    sdk.interactive.login_secret(client_id, client_secret, tsg)
    print("--------------------------------")
    print("Script Execution Progress: ")
    print("--------------------------------")
    print("Login to TSG ID {} successful".format(tsg))

def check_mu_status_based_on_user(user):
    mu_status_url="https://pa-us01.api.prismaaccess.com/api/sase/v2.0/resource/custom/query/gp_mobileusers/user_list"

    header = {
            "prisma-tenant": tsg
    }
    sdk._session.headers.update(header)
    payload = {
        "filter": {
        "operator": "AND",
        "rules":
        [
            {"property":"event_time",
            "operator":"between",
            "values":[1673896504693,1673900103693]
            },
            {"property":"gpuser_name",
            "operator":"in",
            "values":[user]
            }
        ]
        }
    }
    send_post(mu_status_url,header,payload)

def check_mu_status_based_on_loc(location):
    mu_status_url="https://pa-us01.api.prismaaccess.com/api/sase/v2.0/resource/custom/query/gp_mobileusers/user_list"

    header = {
            "prisma-tenant": tsg
    }
    sdk._session.headers.update(header)
    payload = {
        "filter": {
        "operator": "AND",
        "rules":
        [
            {"property":"event_time",
            "operator":"between",
            "values":[1673896504693,1673900103693]
            },
            {"property":"user_location_country",
            "operator":"in",
            "values":[location]
            }
        ]
        }
    }
    #print(payload)
    send_post(mu_status_url,header,payload)

def send_post(mu_status_url,header,payload):
    resp = sdk.rest_call(url=mu_status_url, data=payload, method="POST")
    #print(resp)
    dataList = resp.json()["data"]
    #print(resp.json())

    Header = ["GP-User-Name", "User Location", "PA Location", "User Country Location"]
    RList = []
    index = 0
    for data in dataList:
        #print(data)
        RList.append([data['gpuser_name'], data["user_location"], data["pa_location"], data["user_location_country"]])
        index+=1

    table_string = tt.to_string(RList, Header, style=tt.styles.ascii_thin_double)
    print(table_string)


def go():
    parser = argparse.ArgumentParser(description='Checking MU Status')
    parser.add_argument('-t1', '--T1Secret', help='Input secret file in .yml format for the tenant(T1) ')
    parser.add_argument('-option', '--Option', help='user/loc to query based on user or location')
    parser.add_argument('-user', '--User', help='Given a user, check the location from where the user is logged in')  
    parser.add_argument('-loc', '--Location', help='Given a User location country, list the mobile Users')
     
    args = parser.parse_args()
    T1_secret_filepath = args.T1Secret
    option = args.Option
    user = args.User
    location = args.Location

    #Pass the secret of 'from tenant' to login
    sdk_login_to_controller(T1_secret_filepath)

    #Check MU status
    if option == "user":
        check_mu_status_based_on_user(user)
    elif option == "loc":
        check_mu_status_based_on_loc(location)



if __name__ == "__main__":
    go()