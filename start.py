import sys, ptah
from paste.httpserver import serve

if __name__ == '__main__':
    ini = sys.argv[1]
    app = ptah.make_wsgi_app({'settings': ini})
    serve(app, host='0.0.0.0')
