""" permissions """
import ptah
import ptah_app

# permissions
AddPoll = ptah.Permission('devpoll:AddPoll', 'Add poll')
#RetractTheme = ptah.Permission('ploud:RetractTheme', 'Retract theme')
#ManageGallery = ptah.Permission('ploud:ManageGallery', 'Manage gallery')

# Application ACL
APP_ACL = ptah.ACL('devpoll-application', 'Poll application ACL')
#APP_ACL.allow(ptah.Everyone, ptah_app.View)
APP_ACL.allow(ptah.Authenticated, ptah_app.View)
APP_ACL.allow(ptah_app.Manager, ptah_app.ALL_PERMISSIONS)
