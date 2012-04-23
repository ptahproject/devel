""" Page """
import ptah
import sqlalchemy as sqla

import ptahcms as cms
from devapp.permissions import AddPage


class Page(cms.Content):

    __tablename__ = 'ptah_cmsapp_pages'

    __type__ = cms.Type(
        'page',
        title = 'Page',
        description = 'A page in the site.',
        permission = AddPage,
        name_suffix = '.html',
        )

    text = sqla.Column(sqla.UnicodeText,
                       info = {'field_type': 'tinymce', 'missing': ''})


#ptah.view.register_view(
#    context = Page,
#    permission = cms.View,
#    template = ptah.view.template('devapp:templates/page.pt'))
