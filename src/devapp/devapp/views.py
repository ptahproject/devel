from zope import interface
from ptah import view, form, config
from pyramid.httpexceptions import HTTPFound, HTTPNotFound

import ptah

from initialize import ApplicationRoot


view.register_layout(
    'page',
    template = ptah.view.template("templates/layoutpage.pt"))

view.register_layout(
    'ptah-page', parent='workspace',
    template = ptah.view.template("templates/layout-ptahpage.pt"))


class LayoutWorkspace(view.Layout):
    view.layout('workspace', ApplicationRoot, parent="page",
                template=ptah.view.template("templates/layoutworkspace.pt"))

    def update(self):
        self.root = getattr(self.request, 'root', None)
        self.user = ptah.auth_service.get_current_principal()
        self.isAnon = self.user is None
        self.ptahManager = ptah.manage.check_access(ptah.auth_service.get_userid())


class ContentLayout(view.Layout):
    view.layout('', ptah.cms.Node, parent="workspace",
                template=view.template("templates/layoutcontent.pt"))

    def update(self):
        self.actions = ptah.list_uiactions(self.context, self.request)


class DefaultContentView(form.DisplayForm):
    view.pview(
        context = ptah.cms.Content,
        permission = ptah.cms.View,
        template=ptah.view.template("templates/contentview.pt"))
                      
    @property
    def fields(self):
        return self.context.__type__.fieldset

    def form_content(self):
        data = {}
        for name, field in self.context.__type__.fieldset.items():
            data[name] = getattr(self.context, name, field.default)

        return data


class DefaultEditForm(ptah.cms.EditForm):
    view.pview('edit.html', ptah.cms.Content, permission=ptah.cms.ModifyContent)
