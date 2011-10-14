""" This is an example of running Ptah in 1 module. """

import cgi
from paste.httpserver import serve
from memphis import view 
import ptah_cms

view.register_route('show_models', '/show_models')

@view.pyramidview(route='show_models')
def show_models(request):
    models = ptah_cms.Session.query(ptah_cms.Content).all()
    return cgi.escape(str(models))

@view.pyramidview('show_info', context=ptah_cms.Content)
def show_info(context, request):
    return cgi.escape(str(context.info()))
    
@view.pyramidview('list_children', context=ptah_cms.Container)
def list_children(context, request):
    out = []
    for name, child in context.items():
        if isinstance(child, ptah_cms.Container):
            href = '<a href="%slist_children">%s</a>' #XXX extra /?
            href = href % (request.resource_url(child), child.title)
        else:
            href = '<a href="%sshow_info">%s</a>'
            href = href % (request.resource_url(child), child.title)
        out.append(href)
    return '<br />'.join(out)

if __name__ == '__main__':
    """ need to point to your settings.ini file in make_wsgi_app call.
        http://localhost:8080/show_models is url dispatch function.
        http://localhost:8080/list_children is traverser on context
        $resource_url/show_info on either folder or content.
    """
    import ptah
    app = ptah.make_wsgi_app({'settings':r'./ptah.ini'})
    serve(app, host='0.0.0.0')
