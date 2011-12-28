from zope import interface
from ptah import view, form, config
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound, HTTPNotFound

import ptah

from initialize import ApplicationRoot


ptah.layout.register(
    'page', root=ApplicationRoot, renderer="devapp:templates/layoutpage.pt")

ptah.layout.register(
    'ptah-page', root=ApplicationRoot, parent='workspace',
    renderer="devapp:templates/layout-ptahpage.pt")


@ptah.layout('workspace', ApplicationRoot, root=ApplicationRoot, parent="page",
             renderer="devapp:templates/layoutworkspace.pt")

class LayoutWorkspace(ptah.View):

    def update(self):
        self.root = getattr(self.request, 'root', None)
        self.user = ptah.auth_service.get_current_principal()
        self.isAnon = self.user is None
        self.ptahManager = ptah.manage.check_access(
            ptah.auth_service.get_userid(), self.request)


@ptah.layout('', ptah.cms.Node, root=ApplicationRoot, parent="workspace",
             renderer="devapp:templates/layoutcontent.pt")
class ContentLayout(ptah.View):

    def update(self):
        self.actions = ptah.list_uiactions(self.context, self.request)


@view_config(
        context = ptah.cms.Content,
        wrapper = ptah.wrap_layout(),
        permission = ptah.cms.View,
        renderer="devapp:templates/contentview.pt")
class DefaultContentView(form.DisplayForm):

    @property
    def fields(self):
        return self.context.__type__.fieldset

    def form_content(self):
        data = {}
        for name, field in self.context.__type__.fieldset.items():
            data[name] = getattr(self.context, name, field.default)

        return data


@view_config(
    'edit.html', context=ptah.cms.Content, 
    wrapper=ptah.wrap_layout(),
    permission=ptah.cms.ModifyContent)
class DefaultEditForm(ptah.cms.EditForm):
    pass
