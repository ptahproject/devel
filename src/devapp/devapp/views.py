from zope import interface
from ptah import view, form, config
from pyramid.httpexceptions import HTTPFound, HTTPNotFound

import ptah

from initialize import ApplicationRoot


ptah.register_layout(
    'page', renderer="devapp:templates/layoutpage.pt")

ptah.register_layout(
    'ptah-page', parent='workspace',
    renderer="devapp:templates/layout-ptahpage.pt")


@ptah.layout('workspace', ApplicationRoot, parent="page",
             renderer="devapp:templates/layoutworkspace.pt")

class LayoutWorkspace(ptah.View):

    def update(self):
        self.root = getattr(self.request, 'root', None)
        self.user = ptah.auth_service.get_current_principal()
        self.isAnon = self.user is None
        self.ptahManager = ptah.manage.check_access(
            ptah.auth_service.get_userid())


@ptah.layout('', ptah.cms.Node, parent="workspace",
             renderer="templates/layoutcontent.pt")
class ContentLayout(ptah.View):

    def update(self):
        self.actions = ptah.list_uiactions(self.context, self.request)


#@view.pview(
#    context = ptah.cms.Content,
#    permission = ptah.cms.View,
#    renderer="devapp:templates/contentview.pt")
class DefaultContentView(form.DisplayForm):
                      
    @property
    def fields(self):
        return self.context.__type__.fieldset

    def form_content(self):
        data = {}
        for name, field in self.context.__type__.fieldset.items():
            data[name] = getattr(self.context, name, field.default)

        return data


#class DefaultEditForm(ptah.cms.EditForm):
#    view.pview('edit.html', ptah.cms.Content, permission=ptah.cms.ModifyContent)
