from devapp.ptahclient import PtahClient

server = PtahClient('http://localhost:8080/__rest__/', 'admin', '12345')

if not server.login():
    print server.message
else:
    print 'success'
    print server.authtkn

cms = server.applications['']

print cms, cms.__type__


pageType = server.types['page']
print pageType, pageType.title

for field in pageType.fieldset:
    print field


content = cms.create(pageType, 'test-page.html',
                     title = 'Test page',
                     description = 'Description',
                     text = '<h2>Page from rest</h2>')

content.update(title = 'Test page modified',
               text = '<h2>Page from rest</h2> <br /> Modified')


fileType = server.types['file']

cms.create(fileType, 'repoze.gif', 
           title = 'Test file',
           description = '',
           blobref = open('repoze.gif', 'rb'))
