from dataclasses import dataclass
from email import header
import json
from nturl2path import url2pathname
from urllib import response
from wsgiref import headers
import requests
import restapi

def get_device():
    url = "https://10.215.26.122/api/v1/network-device"
    headers = {
        "X-Auth-Token":restapi.get_ticket()
    }
    data = {
    }
    response = requests.get(url,headers=headers,data=data,verify=False)
    data = response.json()
    #print(json.dumps(data, indent = 4))
    print(len(data['response']))
    for i in range(0,len(data['response'])):
        print(data['response'][i]['type'])
get_device()