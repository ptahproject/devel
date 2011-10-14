from paste.httpserver import serve
import sqlalchemy as sqla
from pyramid.request import Request

from memphis import config, view
import ptah
import ptah_cms

FOO = ptah_cms.ApplicationFactory(
    '/foo', 'foo', 'Foo Application')

view.registerRoute(
    'foo', '/foo/*traverse', factory = FOO, use_global_views = True)

if __name__ == '__main__':
    app = ptah.make_wsgi_app({'settings':r'./ptah.ini'})

    request = Request.blank('/')
    foo = FOO()
    request.root = foo
    request.registry = app.registry

    from ptah_app.content import Page
    if 'page1' not in foo:
        page1 = foo.create(Page.__type__.__uri__, 'page1', 
                           text='<p> some html</p>')
        print'page1', foo['page1'], request.resource_url(page1)

    # We can use SQLAlchemy and Container API, which will notify
    if 'page2' not in foo:
        page2 = Page(text='</p>page 2 html</p>')
        ptah_cms.Session.add(page2)
        foo['page2'] = page2
        print 'page2', foo['page2']
    
    # We can just use SQLAlchemy and manually notify application
    #if not ptah_cms.Session.query(Page).filter_by(__name__='page3').all():
    if 'page3' not in foo:
        page3 = Page(text='<p>page 3 html</p>', 
                     __name__ = 'page3',
                     __parent__ = foo)
        ptah_cms.Session.add(page3)
        config.notify(ptah_cms.events.ContentCreatedEvent(page3))
        import transaction; transaction.commit()
    
    print 'See foo Application, http://localhost:8080/foo/'
    serve(app, '0.0.0.0')
