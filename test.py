from email import header
import re
from matplotlib.style import use
import requests
import json

url = "https://reqres.in/api/unknown"
headers = {}
data = {}

response = requests.get(url,headers=headers, data=data)
print(type(response))
response = response.json() #convert to dict type format
print(type(response))
print(json.dumps(response, indent=4))
users = response['support']['url']
print(response['data'][0]['name'])
print(type(response['support']))
print(users)
