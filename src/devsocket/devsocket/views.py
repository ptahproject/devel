#-----------------------------------------------------------------------------#
#   views.py                                                                  #
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


import gevent

from pyramid.renderers import render_to_response
from pyramid.response import Response
from pyramid.view import view_config
from pyramid_socketio.io import SocketIOContext
from pyramid_socketio.io import socketio_manage


_messages = []


@view_config(route_name='views.home', request_method='GET', renderer='string')
def home_view(request):
    return render_to_response('templates/home.pt', {}, request=request)


@view_config(route_name='views.broadcast', renderer='string')
def broadcast_view(request):
    message = request.POST.get('message')
    if message is None:
        message = request.GET.get('message')
    if message:
        _messages.append(message)


class ConnectIOContext(SocketIOContext):

    def msg_connect(self, msg):
        print "connect message received", msg
        def broadcast():
            index = len(_messages)
            while self.io.connected():
                while index < len(_messages):
                    self.msg('message', message=_messages[index])
                    index += 1
                gevent.sleep(0.5)
        self.spawn(broadcast)


@view_config(route_name="views.socket_io")
def socketio_service(request):
    print "socket.io request running"
    return_value = socketio_manage(ConnectIOContext(request))
    return Response(return_value)
