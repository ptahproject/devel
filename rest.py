from devapp.ptahclient import PtahClient

server = PtahClient('http://localhost:8080/__rest__/', 'admin', '12345')

if not server.login():
    print server.message
else:
    print 'success'
    print server.authtkn
    
