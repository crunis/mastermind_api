#!/usr/local/bin/python
from flup.server.fcgi import WSGIServer
from server import app

if __name__ == '__main__':
    WSGIServer(app, bindAddress='/sockets/mastermind.sock', umask=0000).run()