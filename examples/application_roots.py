""" !!! THIS DOES NOT WORK !!!

    An application located at /foo/ .
    /foo will be an ApplicationRoot without AuthPolicy
"""

from paste.httpserver import serve
from zope import interface
import sqlalchemy as sqla
from memphis import config, view
import ptah
import ptah_cms
import ptah_app

#I really do not want to introduce ApplicationPolicy here.
class ApplicationPolicy(object):
    interface.implements(ptah.ILocalRolesAware,
                         ptah_cms.IApplicationPolicy)
    __name__ = ''
    __parent__ = None
    __acls__ = ['']
    __acl__ = ptah.ACLsProperty()
    __local_roles__ = {'runyaga':ptah_app.Manager.id}

    def __init__(self, request):
        self.request = request

    
FOO = ptah_cms.ApplicationFactory(
    '/foo', 'foo', 'Foo Application', policy=ApplicationPolicy)

view.registerRoute(
    'foo', '/foo/*traverse', factory = FOO, use_global_views = True)


if __name__ == '__main__':
    app = ptah.make_wsgi_app({'settings':r'./ptah.ini'})
    
    foo = FOO() #factory() vs. factory(None)?
    
    #Detour. We need a security context since ptah_cms.Container.create has security
    #ptah.authService.set_userid('runyaga')
    
    from ptah_app.content import Page
    # We can use the Container API
    # Currently we cannot due to security
    if 'page1' not in foo:
        page1 = foo.create(Page.__type__.__uri__, 'page1', 
                           text='<p> some html</p>')
    
    # We can use SQLAlchemy and Container API, which will notify
    if 'page2' not in foo:
        page2 = Page(text='</p>page 2 html</p>')
        ptah_cms.Session.add(page2)
        foo['page2'] = page2
        print 'page2', foo['page2']
    
    # We can just use SQLAlchemy and manually notify application
    # This is borken as well.
    #if not ptah_cms.Session.query(Page).filter_by(__name__='page3').all():
    if 'page3' not in foo:
        page3 = Page(text='<p>page 3 html</p>', 
                     __name__ = 'page3',
                     __parent__ = foo)
        ptah_cms.Session.add(page3)
        config.notify(ptah_cms.events.ContentCreatedEvent(page3))
        import transaction; transaction.commit()

        foo = FOO() #factory() vs. factory(None)?
        print 'page3', foo['page3']
    
    #No idea why filter and filter_by not working with ApplicationRoot.__name__
    serve(app, '0.0.0.0')
