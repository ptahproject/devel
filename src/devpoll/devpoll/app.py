""" poll application """
import sqlalchemy as sqla
from zope import interface

import ptah
import ptah_cms
import ptah_app

from poll import Poll
from permissions import APP_ACL


class PollApplicationPolicy(ptah_cms.ApplicationPolicy):

    __acl__ = APP_ACL


class PollApplication(ptah_cms.Container):
    interface.implements(ptah_app.IPtahAppRoot)

    __name__ = ''

    __type__ = ptah_cms.Type(
        'devpoll-application',
        'Poll application',
        filter_content_types = True,
        allowed_content_types = (Poll.__type__,))

    _sql_values = ptah.QueryFreezer(
        lambda: ptah_cms.Session.query(Poll))

    def values(self):
        return self._sql_values.all()


pollAppFactory = ptah_cms.ApplicationFactory(
    '/polls/', 'polls', 'Polls',  PollApplication, PollApplicationPolicy)
