from zope import interface
from ptah import view, form, config
from pyramid.httpexceptions import HTTPFound, HTTPNotFound

import ptah

from initialize import ApplicationRoot


view.register_layout(
    'page', renderer="templates/layoutpage.pt")

view.register_layout(
    'ptah-page', parent='workspace',
    renderer="templates/layout-ptahpage.pt")


@view.layout('workspace', ApplicationRoot, parent="page",
             renderer="templates/layoutworkspace.pt")

class LayoutWorkspace(view.Layout):

    def update(self):
        self.root = getattr(self.request, 'root', None)
        self.user = ptah.auth_service.get_current_principal()
        self.isAnon = self.user is None
        self.ptahManager = ptah.manage.check_access(ptah.auth_service.get_userid())


@view.layout('', ptah.cms.Node, parent="workspace",
             renderer="templates/layoutcontent.pt")
class ContentLayout(view.Layout):

    def update(self):
        self.actions = ptah.list_uiactions(self.context, self.request)


class DefaultContentView(form.DisplayForm):
    #view.pview(
    #    context = ptah.cms.Content,
    #    permission = ptah.cms.View,
    #    template=ptah.view.template("templates/contentview.pt"))
                      
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
