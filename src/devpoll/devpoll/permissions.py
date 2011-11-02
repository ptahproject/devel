""" permissions """
import ptah

# permissions
AddPoll = ptah.Permission('devpoll:AddPoll', 'Add poll')
#RetractTheme = ptah.Permission('ploud:RetractTheme', 'Retract theme')
#ManageGallery = ptah.Permission('ploud:ManageGallery', 'Manage gallery')

# Application ACL
APP_ACL = ptah.ACL('devpoll-application', 'Poll application ACL')
APP_ACL.allow(ptah.Everyone, ptah.cms.View)
APP_ACL.allow(ptah.Authenticated, ptah.cms.View)
#APP_ACL.allow(ptah.cms.Manager, ptah.cms.ALL_PERMISSIONS)
