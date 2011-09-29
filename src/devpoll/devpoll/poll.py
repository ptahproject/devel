""" poll """
import ptah
import ptah_cms
import colander
import sqlalchemy as sqla
from memphis import config

import permissions


class Poll(ptah_cms.Node):
    
    __tablename__ = 'devapp_polls'
    __id__ = sqla.Column(
        'id', sqla.Integer,
        sqla.ForeignKey('ptah_cms_nodes.id'), primary_key=True)

    title = sqla.Column(
        sqla.Unicode(), default=u'',
        info = {'title': 'Title',
                'widget': 'text' })

    description = sqla.Column(
        sqla.Unicode(), default=u'',
        info = {'title': 'Title',
                'widget': 'textarea'})

    choices = sqla.Column(
        ptah.JsonListType(), default=[],
        info = {'node': colander.SchemaNode(
                colander.Sequence(), colander.SchemaNode(colander.Str()),
                title = 'Choices',
                widget = 'textlines'),
                }
        )

    __type__ = ptah_cms.Type(
        'devpoll-poll', 'Poll',
        permission = permissions.AddPoll,
        add = 'addpoll.html',
        global_allow = False)


    _sql_get = ptah.QueryFreezer(
        lambda: ptah_cms.Session.query(Poll)\
            .filter(Poll.__id__ == sqla.sql.bindparam('id')))

    @classmethod
    def get(cls, id):
        return Poll._sql_get.one(id = id)

    def vote(self, choice):
        pass
