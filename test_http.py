#!/usr/bin/env python3
#-*- coding: utf-8 -*-
import requests
import json

#Создания последовательности
url = 'http://127.0.0.1:8080/sequence/create'
r = requests.post(url)
print(r.status_code, r.content)
assert r.status_code == 200
answer = json.loads(r.content.decode('utf-8'))
sequence = ''
if 'status' in answer and answer['status'] == 'ok':
	sequence = answer['response']['sequence']
else:
	exit -1

# Данные #1
url = 'http://127.0.0.1:8080/observation/add'
payload = {'observation': {'color':'green', 'numbers': ['1110111', '0011101']}, 'sequence':sequence}
r = requests.post(url, data = json.dumps(payload).encode('utf-8'))
print(r.status_code, r.content)
assert r.status_code == 200
assert json.loads(r.content.decode('utf-8')) == {"response": {"start": [8, 2, 88, 82], "missing": ["0000000", "1000000"]}, "status": "ok"}

# Данные №2
url = 'http://127.0.0.1:8080/observation/add'
payload = {'observation': {'color':'green', 'numbers': ['1110111', '0010000']}, 'sequence':sequence}
r = requests.post(url, data = json.dumps(payload).encode('utf-8'))
print(r.status_code, r.content)
assert r.status_code == 200
assert json.loads(r.content.decode('utf-8')) == {"response": {"start": [8, 2, 88, 82], "missing": ["0000000", "1000010"]}, "status": "ok"}

# Данные №3
url = 'http://127.0.0.1:8080/observation/add'
payload = {'observation': {'color':'red'}, 'sequence':sequence}
r = requests.post(url, data = json.dumps(payload).encode('utf-8'))
print(r.status_code, r.content)
assert r.status_code == 200
assert json.loads(r.content.decode('utf-8')) == {"response": {"start": [2], "missing": ["0000000", "1000010"]}, "status": "ok"}

# Кривой запрос на добавление данных
url = 'http://127.0.0.1:8080/observation/add'
payload = 'test=test'
r = requests.post(url, data = json.dumps(payload).encode('utf-8'))
print(r.status_code, r.content)
assert r.status_code == 200
assert json.loads(r.content.decode('utf-8')) == {"status": "error", "msg": "Bad data: no sequence"}

# Неверное URI
url = 'http://127.0.0.1:8080/bla_bla'
payload = 'privet'
r = requests.post(url, data = json.dumps(payload).encode('utf-8'))
print(r.status_code, r.content)
assert r.status_code == 404

# Очистка
url = 'http://127.0.0.1:8080/clear'
r = requests.post(url)
print(r.status_code, r.content)
assert json.loads(r.content.decode('utf-8')) == {"response": "ok", "status": "ok"}

# Get-запрос
url = 'http://127.0.0.1:8080'
r = requests.get(url)
print(r.status_code, r.content)
assert r.status_code == 200

url = 'http://127.0.0.1:8080/observation/add'
payload = {'observation': {'color':'green', 'numbers': ['1110111', '0011101']}, 'sequence':'1'}
r = requests.post(url, data = json.dumps(payload).encode('utf-8'))
print(r.status_code, r.content)
assert r.status_code == 200
assert json.loads(r.content.decode('utf-8')) == {"status": "error", "msg": "The sequence isn't found"}