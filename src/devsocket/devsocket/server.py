#-----------------------------------------------------------------------------#
#   server.py                                                                 #
#                                                                             #
#   Copyright (c) 2011, Enfold Systems, Inc.                                  #
#   All rights reserved.                                                      #
#                                                                             #
#       Authors:                                                              #
#       Raj Shah (raj@enfoldsystems.com)                                      #
#                                                                             #
#           This software is licensed under the Terms and Conditions          #
#           contained within the "LICENSE.txt" file that accompanied          #
#           this software.  Any inquiries concerning the scope or             #
#           enforceability of the license should be addressed to:             #
#                                                                             #
#               Enfold Systems, Inc.                                          #
#               4617 Montrose Blvd., Suite C215                               #
#               Houston, Texas 77006 USA                                      #
#               p. +1 713.942.2377 | f. +1 832.201.8856                       #
#               www.enfoldsystems.com                                         #
#               info@enfoldsystems.com                                        #
#-----------------------------------------------------------------------------#


import gevent.monkey
gevent.monkey.patch_all()


import argparse
import socketio
import sys

from pyramid.config import Configurator


HOST = '0.0.0.0'
PORT = 9090


def make_app(**settings):
    config = Configurator(settings=settings)
    config.add_route('views.broadcast', '/broadcast')
    config.add_route('views.socket_io', '/socket.io/*remaining')
    config.scan('devsocket.views')
    app = config.make_wsgi_app()
    return app


def serve_gevent(app, host=HOST, port=PORT):
    server = socketio.SocketIOServer((host, port), app, resource='socket.io')
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.kill()


def main():
    settings = {}
    app = make_app(**settings)
    serve_gevent(app)


if __name__ == '__main__':
    main()
