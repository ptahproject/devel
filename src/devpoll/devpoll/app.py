""" poll application """
import ptah
import sqlalchemy as sqla
from zope import interface

from poll import Poll
from permissions import APP_ACL


class PollApplicationPolicy(ptah.cms.ApplicationPolicy):

    __acl__ = APP_ACL


class PollApplication(ptah.cms.ApplicationRoot):

    __name__ = ''

    __type__ = ptah.cms.Type(
        'devpoll-application',
        'Poll application',
        filter_content_types = True,
        allowed_content_types = (Poll.__type__,))

    _sql_values = ptah.QueryFreezer(
        lambda: ptah.cms.Session.query(Poll))

    def values(self):
        return self._sql_values.all()


pollAppFactory = ptah.cms.ApplicationFactory(
    PollApplication, '/polls/', 'polls', 'Polls', PollApplicationPolicy)
