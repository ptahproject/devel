""" This is an example of useing form (imperative style). """
import ptah, ptah_cms
from paste.httpserver import serve

from ptah_cms import restAction, View, ModifyContent


@restAction('extra-info', ptah_cms.Content, permission=View)
def extraInfo(content, request):
    """ __doc__ is used for action description """
    
    return {'title': content.title,
            'email': 'ptah@ptahproject.org',
            'message': 'Ptah rest api'}


@restAction('protected-info', ptah_cms.Content, permission=ModifyContent)
def protectedInfo(content, request):
    """ protected rest action """
    
    return {'title': content.title,
            'email': 'ptah@ptahproject.org',
            'message': 'Ptah rest api'}


if __name__ == '__main__':
    """ ...
    
    """
    app = ptah.make_wsgi_app({'settings':r'./ptah.ini'})
    serve(app, host='0.0.0.0')
