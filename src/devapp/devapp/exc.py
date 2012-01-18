""" forbidden/notfound view """
import urllib
import ptah
from ptah import view
from pyramid.view import view_config
from pyramid.interfaces import IRootFactory
from pyramid.traversal import DefaultRootFactory
from pyramid.httpexceptions import HTTPFound, HTTPForbidden, HTTPNotFound


@view_config(
    context=HTTPNotFound,
    wrapper=ptah.wrap_layout('ptah-page'),
    renderer='templates/notfound.pt')

class NotFound(view.View):

    def update(self):
        context = getattr(self.request, 'context', None)
        if context is None:
            context = getattr(self.request, 'root', None)

        self.__parent__ = context
        if getattr(self.context, '__parent__', None) is None:
            self.context.__parent__ = context

        MAIL = ptah.get_settings(ptah.CFG_ID_PTAH, self.request.registry)
        self.admin = MAIL['email_from_name']
        self.email = MAIL['email_from_address']
        self.request.response.status = HTTPNotFound.code
