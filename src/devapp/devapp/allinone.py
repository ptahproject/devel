""" This is an example of running Ptah in 1 module. """

from paste.httpserver import serve
from pyramid.response import Response
from memphis import config, view
import ptah 

@view.pyramidView(route='/show_models')
def hello_models(request):
    from ptah_cms import Session, Content
    models = Session.query(Content).all()
    retun Response(str(models))

if __name__ == '__main__':
    app = ptah.make_wsgi_app({'settings':r'./ptah.ini'})
    serve(app, host='0.0.0.0')
