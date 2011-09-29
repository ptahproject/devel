""" custom config """
from memphis import config, view
from zope import interface

import ptah, ptah_cms
from ptah.crowd.provider import CrowdUser, Session
from ptah_app.content.page import Page, AddPage
from ptah_app.content.folder import Folder

acl = ptah.ACL('simple-map', 'Simple permissions map')
acl.allow(ptah.Everyone, AddPage)


class ApplicationPolicy(object):
    interface.implements(view.INavigationRoot,
                         ptah.ILocalRolesAware,
                         ptah_cms.IApplicationPolicy)

    __name__ = ''
    __parent__ = None

    __acls__ = ['simple-map', '']
    
    __acl__ = ptah.ACLsProperty()

    __local_roles__ = {}

    def __init__(self, request):
        self.request = request


@config.handler(ptah.WSGIAppInitialized)
def initialize(ev):
    pconfig = ev.config

    pconfig.add_route('test-welcome', '/welcome.html')
    pconfig.add_view(route_name='test-welcome', renderer='devapp:welcome.pt')

    # mount cms to /second/
    pconfig.add_route(
        'second-app', '/second/*traverse', 
        factory = ptah_cms.ApplicationFactory(
            '/second/', 'second', 'Test subpath CMS'),
        use_global_views = True)

    # mount cms to /third/cms/
    pconfig.add_route(
        'third-app', '/third/cms/*traverse', 
        factory = ptah_cms.ApplicationFactory(
            '/third/cms/', 'third-app', 'CMS'),
        use_global_views = True)

    # mount cms to /cms/
    factory = ptah_cms.ApplicationFactory('/cms/', 'root', 'Ptah CMS')
    pconfig.add_route(
        'root-app', '/cms/*traverse', 
        factory = factory, use_global_views = True)

    # mount same 'root' application to '/' location
    factory = ptah_cms.ApplicationFactory(
        '/', 'root', 'Ptah CMS', policy=ApplicationPolicy)
    pconfig.add_route(
        'root-app2', '/*traverse', 
        factory = factory, use_global_views = True)

    # some more setup
    root = factory(None)

    # admin user
    user = Session.query(CrowdUser).first()
    if user is None:
        user = CrowdUser('Ptah admin','admin','admin@ptahproject.org','12345')
        Session.add(user)

    ApplicationPolicy.__local_roles__ = {user.uri: ['role:manager']}

    # give manager role to admin
    #if user.uuid not in root.__local_roles__:
    #    root.__local_roles__[user.uuid] = ['role:manager']
    #if 'simple-map' not in root.__permissions__:
    #    root.__permissions__ = ['simple-map']

    # create default page
    if 'front-page' not in root.keys():
        page = Page(title=u'Welcome to Ptah')
        page.text = open(
            view.path('devapp:welcome.pt')[0], 'rb').read()

        Session.add(page)
        config.notify(ptah_cms.events.ContentCreatedEvent(page))

        root['front-page'] = page

    # create folder in root
    if 'folder' not in root.keys():
        folder = Folder(title='Test folder')
        root['folder'] = folder
        Session.add(folder)
        config.notify(ptah_cms.events.ContentCreatedEvent(folder))

        page = Page(title=u'Welcome to Ptah')
        page.text = open(
            view.path('devapp:welcome.pt')[0], 'rb').read()

        Session.add(page)
        config.notify(ptah_cms.events.ContentCreatedEvent(page))

        folder['front-page'] = page

        # set default view for folder
        folder.view = page.__uri__
