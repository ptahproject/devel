""" permissions """
import ptah
import ptah.cmsapp

# permissions
AddPoll = ptah.Permission('devpoll:AddPoll', 'Add poll')
#RetractTheme = ptah.Permission('ploud:RetractTheme', 'Retract theme')
#ManageGallery = ptah.Permission('ploud:ManageGallery', 'Manage gallery')

# Application ACL
APP_ACL = ptah.ACL('devpoll-application', 'Poll application ACL')
#APP_ACL.allow(ptah.Everyone, ptah.cmsapp.View)
APP_ACL.allow(ptah.Authenticated, ptah.cmsapp.View)
APP_ACL.allow(ptah.cmsapp.Manager, ptah.cmsapp.ALL_PERMISSIONS)
