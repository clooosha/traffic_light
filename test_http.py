#-*- coding: utf-8 -*-
import requests
import json

url = 'http://127.0.0.1:8080/sequence/create'
r = requests.post(url)
print(r.status_code, r.content)

url = 'http://127.0.0.1:8080/observation/add'
payload = {'observation': {'color':'green', 'numbers': ['1110111', '0011101']}, 'sequence':'0'}
data = json.dumps(payload)
print (data, json.loads(data))
r = requests.post(url, data = json.dumps(payload))
print(r.status_code, r.content)

url = 'http://127.0.0.1:8080/observation/add'
payload = 'dfgdfgdf'
r = requests.post(url, data = json.dumps(payload))
print(r.status_code, r.content)

url = 'http://127.0.0.1:8080/bla_bla'
payload = 'privet'
r = requests.post(url, data = json.dumps(payload))
print(r.status_code, r.content)

url = 'http://127.0.0.1:8080/clear'
r = requests.post(url)
print(r.status_code, r.content)
