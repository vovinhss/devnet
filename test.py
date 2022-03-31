from email import header
import requests
import json

url = "https://reqres.in/api/unknown"
headers = {}
data = {}

response = requests.get(url,headers=headers, data=data)
print(type(response))
response = response.json()
print(type(response))
#print(json.dumps(response, indent=4))