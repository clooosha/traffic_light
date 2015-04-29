#!/usr/bin/env python3
import sys, time
import signal
from daemon import Daemon
import http.server
from class_http import Handler_http
 
class MyDaemon(Daemon):
        def run(self):
            def signal_handler(signum, frame):
                print ("^C received, shutting down server")
                server.socket.close()
                Handler_http.save_data(Handler_http)
                exit(0)

            signal.signal(signal.SIGTERM, signal_handler)
            signal.signal(signal.SIGINT, signal_handler)


            Handler_http.read_data(Handler_http)
            server = http.server.HTTPServer(("", 8080), Handler_http)
            print ("started httpserver...")
            server.serve_forever()
 
if __name__ == "__main__":
        daemon = MyDaemon("/tmp/traffic_light.pid")
        if len(sys.argv) == 2:
                if 'start' == sys.argv[1]:
                        daemon.start()
                elif 'stop' == sys.argv[1]:
                        daemon.stop()
                elif 'restart' == sys.argv[1]:
                        daemon.restart()
                else:
                        print ("Unknown command")
                        sys.exit(2)
                sys.exit(0)
        else:
                print ("usage: %s start|stop|restart" % sys.argv[0])
                sys.exit(2)



































import http.server
import signal
from class_http import Handler_http

def signal_handler(signum, frame):
    print ("^C received, shutting down server")
    server.socket.close()
    Handler_http.save_data(Handler_http)
    exit(0)

signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGINT, signal_handler)


Handler_http.read_data(Handler_http)
server = http.server.HTTPServer(("", 8080), Handler_http)
print ("started httpserver...")
server.serve_forever()

