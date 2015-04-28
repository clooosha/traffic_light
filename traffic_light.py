#-*- coding: utf-8 -*-
import http.server
from class_light import Light
from class_http import Handler_http
"""a = Light(0)
print a.analyze('green', '1110111', '0011101')
print a.analyze('green', '1110111', '0010000')
print a.analyze('red')"""
try:
	server = http.server.HTTPServer(("", 8080), Handler_http)
	print ("started httpserver...")
	server.serve_forever()
except KeyboardInterrupt:
	print ("^C received, shutting down server")
	Handler_http.save_data(Handler_http)
	server.socket.close()