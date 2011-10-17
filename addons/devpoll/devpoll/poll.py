""" poll """
import ptah
import ptah_cms
import sqlalchemy as sqla
from ptah import config, form

import permissions


class Poll(ptah_cms.Node):

    __tablename__ = 'devapp_polls'
    __id__ = sqla.Column(
        'id', sqla.Integer,
        sqla.ForeignKey('ptah_cms_nodes.id'), primary_key=True)

    title = sqla.Column(
        sqla.Unicode(), default=u'',
        info = {'title': 'Title'})

    description = sqla.Column(
        sqla.Unicode(), default=u'',
        info = {'title': 'Title',
                'field_type': 'textarea'})

    choices = sqla.Column(
        ptah.JsonListType(), default=[],
        info = {'field': form.LinesField('choices', title = 'Choices')}
        )

    __type__ = ptah_cms.Type(
        'devpoll-poll', 'Poll',
        add = 'addpoll.html',
        permission = permissions.AddPoll)

    _sql_get = ptah.QueryFreezer(
        lambda: ptah_cms.Session.query(Poll)\
            .filter(Poll.__id__ == sqla.sql.bindparam('id')))

    @classmethod
    def get(cls, id):
        return Poll._sql_get.one(id = id)

    def vote(self, choice):
        pass
