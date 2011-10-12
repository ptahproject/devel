import sys, ptah
from paste.httpserver import serve
from pyramid.config import Configurator
import ptah_cms

def inituser():
    """if no user exists create one, login/password: admin/12345"""
    from ptah_crowd.provider import CrowdUser
    
    user = ptah_cms.Session.query(CrowdUser).first()
    if user is None:
        user = CrowdUser('Ptah admin','admin','admin@ptahproject.org','12345')
        ptah_cms.Session.add(user)
        import transaction; transaction.commit()

if __name__ == '__main__':
    ini = sys.argv[1]
    
    # Initialize Ptah and make available http://localhost:8080/ptah-manage 
    config = Configurator(settings={'settings':ini})
    config.include('ptah')
    config.ptah_init()
    
    # Mounts / to Ptah Application
    root = ptah_cms.ApplicationFactory(name='root', title='Ptah Application')
    config.set_root_factory(root)    
    app = config.make_wsgi_app()
    
    inituser() # create admin/12345
    
    # http://localhost:8080/ptah-mannage and login with admin/12345
    serve(app, host='0.0.0.0')
