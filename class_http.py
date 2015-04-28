#-*- coding: utf-8 -*-
from http.server import BaseHTTPRequestHandler, HTTPServer
import http.client
import hashlib
from class_light import Light
import json
import pickle

class Handler_http(BaseHTTPRequestHandler):
	sequences = {}
	print ("Reading data...")
	try:
		f = open('data.pickle', 'rb')
		sequences = pickle.load(f)
		print("Found sequences:", len(sequences))
	except:
		print("Error.")
	def create_sequence(self):
		sequence = hashlib.md5(str(len(Handler_http.sequences)).encode('utf-8')).hexdigest()
		print (sequence)
		Handler_http.sequences[sequence] = Light()
		return sequence

	def analyze_data(self, data):
		if 'sequence' in data:
			if not (data['sequence'] in Handler_http.sequences):
				return ('error', "The sequence isn't found")
		else:
			return ('error', 'Bad data: no sequence')

		if 'observation' in data:
			if 'color' in data['observation']:
				if data['observation']['color'] == 'red':
					return Handler_http.sequences[data['sequence']].analyze(color = 'red')
				elif data['observation']['color'] == 'green':
					if 'numbers' in data['observation']:
						if len(data['observation']['numbers']) == 2:
							return Handler_http.sequences[data['sequence']].analyze('green', data['observation']['numbers'])
						else:
							return ('error', 'Bad data: errors in numbers')
					else:
						return ('error', 'Bad data: no numbers')
				else:
					return ('error', 'Bad data: errors in color')
			else:
				return ('error', 'Bad data: no color')
		else:
			return ('error', 'Bad data: no observation')

	def do_GET(self):
		self.send_response(200)
		self.end_headers()

	def do_POST(self):
		if self.path == '/sequence/create':
			self.send_response(200)
			self.end_headers()
			sequence = self.create_sequence()
			answer = {'status': 'ok', 'response':{'sequence':sequence}}
			print("Output data: ", answer)
			self.wfile.write(json.dumps(answer).encode('utf-8'))
		elif self.path == '/observation/add':
			data = self.rfile.read(int(self.headers['Content-Length']))
			try:
				data = json.loads(data.decode('utf-8'))
			except:
				self.send_response(200)
				self.end_headers()
				answer = {'status':'error', 'msg':'Bad data'}
				print(json.dumps(answer))
				self.wfile.write(json.dumps(answer).encode('utf-8'))
				return
			print ("Input data: ", data)
			res = self.analyze_data(data)
			if res[0] == 'ok':
				answer = {'status': res[0], 'response': {'start': res[1], 'missing':[res[2], res[3]]}}
			else:
				answer = {'status': res[0], 'msg': res[1]}
			print("Output data: ", answer)
			self.send_response(200)
			self.end_headers()
			self.wfile.write(json.dumps(answer).encode('utf-8'))
		elif self.path == '/clear':
			Handler_http.sequences = {}
			self.send_response(200)
			self.end_headers()
			answer = {'status': 'ok', 'response':'ok' }
			print("Output data: ", answer)
			self.wfile.write(json.dumps(answer).encode('utf-8'))
		else:
			self.send_response(404)
			self.end_headers()

	def save_data(self):
		print("Saving..")
		with open('data.pickle', 'wb') as f:
			pickle.dump(Handler_http.sequences, f)
