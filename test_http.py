#-*- coding: utf-8 -*-
import requests
import json

url = 'http://127.0.0.1:8080/sequence/create'
r = requests.post(url)
print(r.status_code, r.content)
answer = json.loads(r.content.decode('utf-8'))

sequence = ''
if 'status' in answer and answer['status'] == 'ok':
	sequence = answer['response']['sequence']
else:
	exit -1

url = 'http://127.0.0.1:8080/observation/add'
payload = {'observation': {'color':'green', 'numbers': ['1110111', '0011101']}, 'sequence':sequence}
r = requests.post(url, data = json.dumps(payload).encode('utf-8'))
print(r.status_code, r.content)

url = 'http://127.0.0.1:8080/observation/add'
payload = {'observation': {'color':'green', 'numbers': ['1110111', '0010000']}, 'sequence':sequence}
r = requests.post(url, data = json.dumps(payload).encode('utf-8'))
print(r.status_code, r.content)

url = 'http://127.0.0.1:8080/observation/add'
payload = {'observation': {'color':'red'}, 'sequence':sequence}
r = requests.post(url, data = json.dumps(payload).encode('utf-8'))
print(r.status_code, r.content)

url = 'http://127.0.0.1:8080/observation/add'
payload = 'test=test'
r = requests.post(url, data = json.dumps(payload).encode('utf-8'))
print(r.status_code, r.content)

url = 'http://127.0.0.1:8080/bla_bla'
payload = 'privet'
r = requests.post(url, data = json.dumps(payload).encode('utf-8'))
print(r.status_code, r.content)

url = 'http://127.0.0.1:8080/clear'
r = requests.post(url)
print(r.status_code, r.content)

url = 'http://127.0.0.1:8080'
r = requests.get(url)
print(r.status_code, r.content)