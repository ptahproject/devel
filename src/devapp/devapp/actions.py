""" default actions """
import ptah
import ptahcms

ptah.uiaction(
    ptahcms.IContent, **{'id': 'view',
                          'title': 'View',
                          'action': '',
                          'permission': ptahcms.View,
                          'sort_weight': 0.5})

ptah.uiaction(
    ptahcms.IContent, **{'id': 'edit',
                          'title': 'Edit',
                          'action': 'edit.html',
                          'permission': ptahcms.ModifyContent,
                          'sort_weight': 0.6})


ptah.uiaction(
    ptahcms.IContainer, **{'id': 'adding',
                            'title': 'Add content',
                            'action': '+/',
                            'permission': ptahcms.AddContent,
                            'sort_weight': 5.0})


ptah.uiaction(
    ptah.ILocalRolesAware, **{'id': 'sharing',
                              'title': 'Sharing',
                              'action': 'sharing.html',
                              'permission': ptahcms.ShareContent,
                              'sort_weight': 10.0})
