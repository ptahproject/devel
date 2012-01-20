import gevent

from pyramid.view import view_config
from pyramid.httpexceptions import HTTPNotFound
from pyramid.renderers import render_to_response


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


class ConnectJSContext(object): #SockJSContext):

    def msg_connect(self, msg):
        print "connect message received", msg
        def broadcast():
            index = len(_messages)
            while self.io.connected():
                while index < len(_messages):
                    print 'send message:', _messages[index]
                    self.msg('message', message=_messages[index])
                    index += 1
                gevent.sleep(0.5)
        self.spawn(broadcast)
