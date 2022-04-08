import requests
import json
import sdwaninfo

url1 = sdwaninfo.vmanage
username = sdwaninfo.username
password = sdwaninfo.password
def get_cookie():
    url = f"{url1}/j_security_check"
    headers = {
    "Content_Type": "application/x-www-form-urlencoded"
    }
    data = {
        "j_username":username,
        "j_password": password
    }

    response = requests.post(url,headers= headers, data=data, verify=False)
    cookie = response.headers['Set-Cookie']
    jssc = cookie.split(';')[0]
    return jssc
def get_cookie1():
    url = f"{url1}/j_security_check"
    headers = {
    "Content_Type": "application/x-www-form-urlencoded"
    }
    data = {
        "j_username":username,
        "j_password": password
    }
    session = requests.Session()

    response = session.post(url,headers= headers, data=data, verify=False)
    return session
def get_device():
    url = f"{url1}/dataservice/device"
    headers = {
        "Cookie": get_cookie()
    }
    data = {}
    response = requests.get(url,headers=headers,data=data,verify= False)
    print(json.dumps(response.json(), indent = 4))
def get_device1():
    url = f"{url1}/dataservice/device"
    session = get_cookie1()
    data = {}
    response = session.get(url,verify= False)
    print(json.dumps(response.json(), indent = 4))
if __name__ == '__main__':
    get_device1()
