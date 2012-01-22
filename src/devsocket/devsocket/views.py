from pyramid.view import view_config
from pyramid.httpexceptions import HTTPNotFound
from pyramid.renderers import render_to_response


@view_config(route_name='views.home', request_method='GET', renderer='string')
def home_view(request):
    return render_to_response('templates/home.pt', {}, request=request)


@view_config(route_name='views.broadcast', renderer='string')
def broadcast_view(request):
    message = request.POST.get('message')
    if message is None:
        message = request.GET.get('message')
    if message:
        manager = request.get_sockjs_manager()
        manager.broadcast([message])

    return 'Message has been sent' 
