""" app permissions and roles """
import ptah
import ptahcms

AddPage = ptah.Permission('ptah-app: Add page', 'Add page')
AddFile = ptah.Permission('ptah-app: Add file', 'Add file')
AddFolder = ptah.Permission('ptah-app: Add folder', 'Add folder')

ptah.Everyone.allow(ptahcms.View)
ptah.Authenticated.allow(ptahcms.AddContent)

Viewer = ptah.Role('viewer', 'Viewer')
Viewer.allow(ptahcms.View)

Editor = ptah.Role('editor', 'Editor')
Editor.allow(ptahcms.View, ptahcms.ModifyContent)

Manager = ptah.Role('manager', 'Manager')
Manager.allow(ptah.ALL_PERMISSIONS)

ptah.Owner.allow(ptahcms.DeleteContent)
