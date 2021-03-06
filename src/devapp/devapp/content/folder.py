""" Generic folder implementation """
import ptahcms as cms
from devapp.permissions import AddFolder


class Folder(cms.Container):

    __type__ = cms.Type(
        'folder',
        title = 'Folder',
        description = 'A folder which can contain other items.',
        permission = AddFolder)
