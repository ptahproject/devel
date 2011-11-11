""" custom config """
from zope import interface
from ptah import config, view

import ptah
from biga.crowd.provider import CrowdUser, Session

from devapp.content.page import Page, AddPage
from devapp.content.folder import Folder

acl = ptah.ACL('simple-map', 'Simple permissions map')
acl.allow(ptah.Everyone, AddPage)


class ApplicationRoot(ptah.cms.ApplicationRoot):

    __type__ = ptah.cms.Type(
        'app', 'Application',
        description = 'Default ptah application')


class ApplicationPolicy(object):
    interface.implements(ptah.ILocalRolesAware,
                         ptah.cms.IApplicationPolicy)

    __name__ = ''
    __parent__ = None

    __acls__ = ['simple-map', '']

    __acl__ = ptah.ACLsProperty()

    __local_roles__ = {}

    def __init__(self, request):
        self.request = request


view.register_route(
    'ptah-manage-view','/ptah-manage',
    ptah.manage.PtahManageRoute, use_global_views=True)


view.register_route(
    'ptah-manage','/ptah-manage/*traverse',
    ptah.manage.PtahManageRoute, use_global_views=True)


@config.subscriber(config.AppStarting)
def initialize(ev):
    pconfig = ev.config

    pconfig.add_route('test-welcome', '/welcome.html')
    pconfig.add_view(route_name='test-welcome', renderer='devapp:welcome.pt')

    # enable rest api
    ptah.enable_rest_api(pconfig)

    # mount cms to /second/
    pconfig.add_route(
        'second-app', '/second/*traverse',
        factory = ptah.cms.ApplicationFactory(
            ApplicationRoot, '/second/', 'second', 'Test subpath CMS'),
        use_global_views = True)

    # mount cms to /third/cms/
    pconfig.add_route(
        'third-app', '/third/cms/*traverse',
        factory = ptah.cms.ApplicationFactory(
            ApplicationRoot, '/third/cms/', 'third-app', 'CMS'),
        use_global_views = True)

    # mount cms to /cms/
    factory = ptah.cms.ApplicationFactory(
        ApplicationRoot, '/cms/', 'root', 'Ptah CMS')
    pconfig.add_route(
        'root-app', '/cms/*traverse',
        factory = factory, use_global_views = True)

    # mount same 'root' application to '/' location
    factory = ptah.cms.ApplicationFactory(
        ApplicationRoot, '/', 'root', 'Ptah CMS', 
        policy=ApplicationPolicy, default_root=True)
    pconfig.set_root_factory(factory)

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
        config.notify(ptah.cms.events.ContentCreatedEvent(page))

        root['front-page'] = page

    # create folder in root
    if 'folder' not in root.keys():
        folder = Folder(title='Test folder')
        root['folder'] = folder
        Session.add(folder)
        config.notify(ptah.cms.events.ContentCreatedEvent(folder))

        page = Page(title=u'Welcome to Ptah')
        page.text = open(
            view.path('devapp:welcome.pt')[0], 'rb').read()

        Session.add(page)
        config.notify(ptah.cms.events.ContentCreatedEvent(page))

        folder['front-page'] = page

        # set default view for folder
        folder.view = page.__uri__
