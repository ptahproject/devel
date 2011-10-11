""" This is an example of security and URI resolver in 1 module. """

import cgi
from paste.httpserver import serve
from zope import interface
from memphis import view 
import ptah
import ptah_cms

# login name is a ptah.uri.Uri which means its prefixed with a scheme.
# this is login, bobdobbs whose prefix is user+example.  
# the default Ptah implementation is ptah.crowd.provider, scheme `user+crowd`

USERS = {'user+example:bobdobbs':'aliens'}
SCHEME = 'user+example'

# Close your eyes.. checkers is hardwired?!
# Let's labotomize it.. oh wait, cant do it here ;-( must do it in __main__
#from ptah import authentication
#authentication.checkers = []

class User(object):

    def __init__(self, login):
        self.uri = '%s:%s' % (SCHEME, login)
        self.password = USERS.get(self.uri)
        self.login = login
        self.name = login

    @classmethod
    def get(cls, login):
        login = login.split(':',1)[-1]
        
        if USERS.get('%s:%s' % (SCHEME, login)):
            return User(login)

    getByLogin = getById = get

class UserProvider(object):
    interface.implements(ptah.IAuthProvider)

    def authenticate(self, creds):
        login, password = creds['login'], creds['password']
        user = User.get(login)
        if user is not None:
            return user 
    def getPrincipalByLogin(self, login):
        return User(login)

# registration
@ptah.resolver('user+example', 'An example principal resolver')
def getPrincipal(uri):
    return User.get(uri)

ptah.registerProvider('example', UserProvider())

 
if __name__ == '__main__':
    """ need to point to your settings.ini file in make_wsgi_app call.
        http://localhost:8080/show_models is url dispatch function.
        http://localhost:8080/list_children is traverser on context
        $resource_url/show_info on either folder or content.
    """
    #import ptah, will fix
    app = ptah.make_wsgi_app({'settings':r'./ptah.ini'})
    from ptah import authentication
    authentication.checkers = []

    serve(app, host='0.0.0.0')
