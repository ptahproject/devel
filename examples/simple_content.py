from paste.httpserver import serve
import sqlalchemy as sqla
import ptah
import ptah_cms

class Hyperlink(ptah_cms.Content):
    __tablename__ = 'ptah_cms_hyperlink'
    __type__ = ptah_cms.Type('hyperlink', permission=ptah_cms.AddContent)
    href = sqla.Column(sqla.Unicode)

if __name__ == '__main__':
    app = ptah.make_wsgi_app({'settings':r'./ptah.ini'})
    # we are initialized after make_wsgi_app
    if not ptah_cms.Session.query(Hyperlink).first():
        link = Hyperlink(title='ptah project',
                         href='http://ptahproject.org')
        ptah_cms.Session.add(link)
        import transaction; transaction.commit()
        
    for link in ptah_cms.Session.query(Hyperlink).all():
        print 'curl http://localhost:8080/__rest__/cms/content/%s' % link.__uri__
        
    serve(app, host='0.0.0.0')
