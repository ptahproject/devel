from zope import interface
from ptah import view, form, config
from pyramid.httpexceptions import HTTPFound, HTTPNotFound

import ptah
from ptah import authService, manage
from ptah import cms
from ptah.cms import tinfo, interfaces, events

from ptah.cmsapp import AddForm
from ptah.cmsapp import list_uiactions


view.register_layout(
    'page', cms.ApplicationRoot,
    template = view.template("templates/layoutpage.pt"))

view.register_layout(
    'ptah-page', cms.ApplicationRoot, parent='workspace', layer='ptah.cmsapp',
    template = view.template("templates/layout-ptahpage.pt"))


class LayoutWorkspace(view.Layout):
    view.layout('workspace', cms.ApplicationRoot, parent="page",
                template=view.template("templates/layoutworkspace.pt"))

    def update(self):
        self.root = getattr(self.request, 'root', None)
        self.user = authService.get_current_principal()
        self.isAnon = self.user is None
        self.ptahManager = manage.get_access_manager()(authService.get_userid())


class ContentLayout(view.Layout):
    view.layout('', interfaces.IContent, parent="workspace",
                template=view.template("templates/layoutcontent.pt"))

    def update(self):
        self.actions = list_uiactions(self.context, self.request)


class DefaultContentView(form.DisplayForm):
    view.pview(
        context = cms.Content,
        permission = cms.View,
        template=view.template("templates/contentview.pt"))

    @property
    def fields(self):
        return self.context.__type__.fieldset

    def form_content(self):
        data = {}
        for name, field in self.context.__type__.fieldset.items():
            data[name] = getattr(self.context, name, field.default)

        return data