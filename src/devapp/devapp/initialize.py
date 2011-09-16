""" custom config """
from memphis import config, view
from zope.component import getSiteManager

import ptah, ptah_cms
from ptah.crowd.provider import CrowdUser, Session
from ptah_app.content.page import Page, AddPage

pmap = ptah.security.PermissionsMap('simple-map', 'Simple permissions map')
pmap.allow(ptah.security.Everyone, AddPage)


@config.handler(ptah.WSGIAppInitialized)
def initialize(ev):
    config = ev.config

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
    config.add_route(
        'root-app', '/*traverse', 
        factory = factory, use_global_views = True)

    # some more settings
    root = factory(None)

    # admin user
    user = Session.query(CrowdUser).first()
    if user is None:
        user = CrowdUser('Ptah admin','admin','admin@ptahproject.org','12345')
        Session.add(user)

    # give manager role to admin
    if user.uuid not in root.__local_roles__:
        root.__local_roles__[user.uuid] = ['role:manager']

    if 'simple-map' not in root.__permissions__:
        root.__permissions__ = ['simple-map']

    # create default page
    if 'front-page' not in root.keys():
        page = Page(title=u'Welcome to Ptah')
        page.text = open(
            view.path('devapp:welcome.pt')[0], 'rb').read()

        Session.add(page)
        getSiteManager().notify(ptah_cms.events.ContentCreatedEvent(page))

        root['front-page'] = page
        root.view = page.__uuid__
