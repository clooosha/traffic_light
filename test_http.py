#-*- coding: utf-8 -*-
import requests
import json

url = 'http://127.0.0.1:8080/sequence/create'
r = requests.post(url)
print(r.status_code, r.content)

url = 'http://127.0.0.1:8080/observation/add'
payload = {'observation': {'color':'green', 'numbers': ['1110111', '0011101']}, 'sequence':'0'}
r = requests.post(url, data = json.dumps(payload).encode('utf-8'))
print(r.status_code, r.content)

url = 'http://127.0.0.1:8080/observation/add'
payload = {'observation': {'color':'green', 'numbers': ['1110111', '0010000']}, 'sequence':'0'}
r = requests.post(url, data = json.dumps(payload).encode('utf-8'))
print(r.status_code, r.content)

url = 'http://127.0.0.1:8080/observation/add'
payload = {'observation': {'color':'red'}, 'sequence':'0'}
r = requests.post(url, data = json.dumps(payload).encode('utf-8'))
print(r.status_code, r.content)

url = 'http://127.0.0.1:8080/observation/add'
payload = 'dfgdfgdf'
r = requests.post(url, data = json.dumps(payload).encode('utf-8'))
print(r.status_code, r.content)

url = 'http://127.0.0.1:8080/bla_bla'
payload = 'privet'
r = requests.post(url, data = json.dumps(payload).encode('utf-8'))
print(r.status_code, r.content)

url = 'http://127.0.0.1:8080/clear'
r = requests.post(url)
print(r.status_code, r.content)
