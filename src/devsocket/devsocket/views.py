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


from pyramid.response import Response
from pyramid.view import view_config
from pyramid_socketio.io import SocketIOContext
from pyramid_socketio.io import socketio_manage


@view_config(route_name='views.broadcast', request_method='POST', renderer='string')
def broadcast_view(request):
    event_name = request.POST.get('event_name')
    if event_name:
        pass


class ConnectIOContext(SocketIOContext):
    # self.io is the Socket.IO socket
    # self.request is the request
    def msg_connect(self, msg):
        print "Connect message received", msg
        self.msg("connected", hello="world")


# Socket.IO implementation
@view_config(route_name="views.socket_io")
def socketio_service(request):
    print "Socket.IO request running"
    retval = socketio_manage(ConnectIOContext(request))
    return Response(retval)
