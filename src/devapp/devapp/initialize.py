""" custom config """
import transaction
from zope import interface
from pyramid.path import AssetResolver
from pyramid.config import Configurator
from pyramid.events import ApplicationCreated

import ptah
import ptah_crowd

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


@ptah.subscriber(ApplicationCreated)
def initialize(ev):
    pconfig = Configurator(ev.app.registry)

    pconfig.add_route('test-welcome', '/welcome.html')
    pconfig.add_view(route_name='test-welcome', renderer='devapp:welcome.pt')

    # enable rest api
    ptah.enable_rest_api(pconfig)

    # mount cms to /second/
    pconfig.add_route(
        'second-app', '/second/*traverse',
        factory = ptah.cms.ApplicationFactory(
            ApplicationRoot, '/second/', 'second', 'Test subpath CMS', 
            config = pconfig),
        use_global_views = True)

    # mount cms to /third/cms/
    pconfig.add_route(
        'third-app', '/third/cms/*traverse',
        factory = ptah.cms.ApplicationFactory(
            ApplicationRoot, '/third/cms/', 'third-app', 'CMS', config=pconfig),
        use_global_views = True)

    # mount cms to /cms/
    factory = ptah.cms.ApplicationFactory(
        ApplicationRoot, '/cms/', 'root', 'Ptah CMS', config=pconfig)
    pconfig.add_route(
        'root-app', '/cms/*traverse',
        factory = factory, use_global_views = True)

    # mount same 'root' application to '/' location
    factory = ptah.cms.ApplicationFactory(
        ApplicationRoot, '/', 'root', 'Ptah CMS',
        policy=ApplicationPolicy, default_root=True, config=pconfig)
    pconfig.set_root_factory(factory)
    ev.app.root_factory = factory

    # some more setup
    root = factory(None)

    # admin user
    user = ptah.cms.Session.query(ptah_crowd.CrowdUser).first()
    if user is None:
        user = ptah_crowd.CrowdUser(
            title='Ptah admin',
            login='admin',
            email='admin@ptahproject.org',
            password='12345')
        crowd = ptah_crowd.CrowdFactory()
        crowd.add(user)

    ApplicationPolicy.__local_roles__ = {user.__uri__: ['role:manager']}

    resolver = AssetResolver()

    # create default page
    if 'front-page' not in root.keys():
        page = Page(title=u'Welcome to Ptah')
        page.text = open(
            resolver.resolve('welcome.pt').abspath(), 'rb').read()

        ptah.cms.Session.add(page)
        pconfig.registry.notify(ptah.events.ContentCreatedEvent(page))

        root['front-page'] = page

    # create folder in root
    if 'folder' not in root.keys():
        folder = Folder(title='Test folder')
        root['folder'] = folder
        ptah.cms.Session.add(folder)
        pconfig.registry.notify(ptah.events.ContentCreatedEvent(folder))

        page = Page(title=u'Welcome to Ptah')
        page.text = open(
            resolver.resolve('welcome.pt').abspath(), 'rb').read()

        ptah.cms.Session.add(page)
        pconfig.registry.notify(ptah.events.ContentCreatedEvent(page))

        folder['front-page'] = page

        # set default view for folder
        folder.view = page.__uri__

    pconfig.commit()
    transaction.commit()
