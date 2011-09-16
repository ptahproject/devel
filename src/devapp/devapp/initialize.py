""" custom config """
from memphis import config, view

import ptah, ptah_cms
from ptah.crowd.provider import CrowdUser, Session
from ptah_app.content.page import Page


@config.handler(ptah.WSGIAppInitialized)
def initialize(ev):
    config = ev.config

    user = Session.query(CrowdUser).first()
    if user is None:
        Session.add(CrowdUser(
            'Ptah admin', 'admin', 'admin@ptahproject.org', '12345'))

    # mount cms to /second/
    config.add_route(
        'second-app', '/second/*traverse', 
        factory = ptah_cms.ApplicationFactory(
            '/second/', 'second', 'Test subpath CMS'),
        use_global_views = True)

    # mount cms to /third/cms/
    config.add_route(
        'third-app', '/third/cms/*traverse', 
        factory = ptah_cms.ApplicationFactory(
            '/third/cms/', 'third-app', 'CMS'),
        use_global_views = True)

    # mount cms to /
    factory = ptah_cms.ApplicationFactory('/', 'root', 'Ptah CMS')

    root = factory(None)
    if 'front-page' not in root.keys():
        page = Page(title=u'Welcome to Ptah', 
                    name=u'front-page', __parent__ = root)
        page.text = open(
            view.path('devapp:welcome.pt')[0], 'rb').read()
        Session.add(page)

    config.add_route(
        'root-app', '/*traverse', 
        factory = factory, use_global_views = True)
