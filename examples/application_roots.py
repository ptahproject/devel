""" Multiple applications in URL.
    /foo will be an ApplicationRoot without AuthPolicy
    /baz will be an ApplicationRoot with AuthPolicy
"""

from paste.httpserver import serve
import sqlalchemy as sqla
from memphis import config
import ptah
import ptah_cms

@config.subscriber(config.AppStarting)
def initialize(ev):
    pconfig = ev.config
    
    factory = ptah_cms.ApplicationFactory('/foo', 'foo', 'Foo Example')
    pconfig.add_route(
        'foo', '/foo/*traverse',
        factory = factory, use_global_views = True)

    print '/foo/ is now an ApplicationRoot'
    
if __name__ == '__main__':
    app = ptah.make_wsgi_app({'settings':r'./ptah.ini'})
    #foo = ptah_cms.Session.query(ptah_cms.ApplicationRoot).filter_by(__name__='foo')
    foo = ptah_cms.Factories['foo']() #factory() vs. factory(None)?
    
    from ptah_app.content import Page
    # We can use the Container API
    page1 = foo.create(Page.__type__.__uri__, 'page1', text='<p> some html</p>')
    
    # We can use SQLAlchemy and Container API
    page2 = Page(text='</p>page 2 html</p>')
    foo['page2'] = page2
    ptah_cms.Session.add(page2)
    
    # We can just use SQLAlchemy
    page3 = Page(text='<p>page 3 html</p>')
    ptah_cms.Session.add(page2, __parent__=foo)
    config.notify(ptah_cms.events.ContentCreatedEvent(page))

    serve(app, '0.0.0.0')


