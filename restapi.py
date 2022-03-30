print(" REST API 30/3/20202")
import requests
import json
def get_ticket():
	url = "https://10.215.26.122/api/v1/ticket"

	header = {

		"Content-Type":"application/json"
	}
	#user_name = input(" Enter the")
	#pass_word = input(" Enter text")
	body = json.dumps({
		"username": "admin",
		"password": "vnpro@149"
	})


	response = requests.post(url,headers=header, data=body, verify=False)
	#response = requests.request("POST", url, headers=header, data=body, verify=False)
	data = response.json()
	print(json.dumps(data, indent = 4))
	#print(type(response))
	#rint(response.text)
	ticket = data['response']['serviceTicket']
	print(ticket)
get_ticket()