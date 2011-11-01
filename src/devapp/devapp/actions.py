""" default actions """
import ptah.cms

ptah.cms.uiaction(
    ptah.cms.IContent, **{'id': 'view',
                          'title': 'View',
                          'action': '',
                          'permission': ptah.cms.View,
                          'sort_weight': 0.5})

ptah.cms.uiaction(
    ptah.cms.IContent, **{'id': 'edit',
                          'title': 'Edit',
                          'action': 'edit.html',
                          'permission': ptah.cms.ModifyContent,
                          'sort_weight': 0.6})


ptah.cms.uiaction(
    ptah.cms.IContainer, **{'id': 'adding',
                            'title': 'Add content',
                            'action': '+/',
                            'permission': ptah.cms.AddContent,
                            'sort_weight': 5.0})


ptah.cms.uiaction(
    ptah.ILocalRolesAware, **{'id': 'sharing',
                              'title': 'Sharing',
                              'action': 'sharing.html',
                              'permission': ptah.cms.ShareContent,
                              'sort_weight': 10.0})
