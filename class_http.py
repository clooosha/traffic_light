#-*- coding: utf-8 -*-
from http.server import BaseHTTPRequestHandler, HTTPServer
import http.client
from class_light import Light
import json

class Handler_http(BaseHTTPRequestHandler):
	sequences = []
	def create_sequence(self):
		Handler_http.sequences.append(Light())
		return len(Handler_http.sequences) -1

	def analyze_data(self, data):
		if 'sequence' in data:
			try:
				num_seq = int(data['sequence'])
			except:
				return ('error', "The sequence isn't found")
		else:
			return ('error', 'Bad data: no sequence')

		if (num_seq >= 0) and (num_seq < len(Handler_http.sequences)):
			if 'observation' in data:
				if 'color' in data['observation']:
					if data['observation']['color'] == 'red':
						return Handler_http.sequences[num_seq].analyze(color = 'red')
					elif data['observation']['color'] == 'green':
						if 'numbers' in data['observation']:
							if len(data['observation']['numbers']) == 2:
								return Handler_http.sequences[num_seq].analyze('green', data['observation']['numbers'])
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
		else:
			return ('error', "The sequence isn't found")

	def do_GET(self):
		self.send_response(200)

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
				answer = {'status':'error', 'msg':'json.decode'}
				print(json.dumps(res))
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
			Handler_http.sequences = []
			self.send_response(200)
			self.end_headers()
			answer = {'status': 'ok', 'response':'ok' }
			print("Output data: ", answer)
			self.wfile.write(json.dumps(answer).encode('utf-8'))
		else:
			self.send_response(404)
			self.end_headers()
