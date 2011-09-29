import socket, errno
import httplib, urllib, urlparse
import simplejson as json

from pprint import pprint

__version__ = '0.1'


TRANSPORT = None

class PtahClient(object):

    def __init__(self, url, login=None, passwd=None, authtkn=None):
        self._login = login
        self._passwd = passwd
        self.authtkn = authtkn

        path = urlparse.urlparse(url).path
        if path.endswith('/'):
            path = path[:-1]

        self.path = path
        self._auth_checked = False
        self.message = ''

        self.transport = Transport(url, authtkn)
        global TRANSPORT
        TRANSPORT = self.transport

    def login(self):
        params = {}

        if self._login:
            params = {'login': self._login,
                      'password': self._passwd}
        else:
            params = {'auth-token': self.authtkn}
        
        status, data = self.transport.request(
            '%s/login'%self.path, params=params)
        if status != 200:
            self.message = data.get('message')
            return False

        self.authtkn = data['auth-token']
        self.transport.set_auth_token(self.authtkn)
        return True

    def _loadTypes(self):
        status, data = self.transport.request(
            '%s/cms/types'%self.path)

        types = {}
        for rec in data:
            types[rec['name']] = UriObject('', rec['__uri__'], **rec)

        self.__dict__['types'] = types

    def _loadApplications(self):
        status, data = self.transport.request(
            '%s/cms/applications'%self.path)

        apps = {}
        for rec in data:
            base = '%s/cms/content:%s'%(self.path, rec['__mount__'])
            apps[rec['__mount__']] = createObj(base, rec)

        self.__dict__['applications'] = apps

    def __getattr__(self, name):
        if name == 'types':
            self._loadTypes()
            return self.types

        if name == 'applications':
            self._loadApplications()
            return self.applications

        raise AttributeError(name)


APIDOC = {}

class UriObject(object):

    def __init__(self, base, uri, **data):
        self.__dict__.update(data)
        self._base = base
        self.__uri__ = uri

    def apidoc(self):
        if self.__type__ in APIDOC:
            return APIDOC[self.__type__]

        # load apidoc
        status, data = TRANSPORT.request(
            '%s/%s/apidoc'%(self._base, self.__uri__))

        print status
        pprint(data)


def createObj(base, data):
    if data.get('__content__'):
        if data.get('__container__'):
            return Container(base, data['__uri__'], **data)
        else:
            return Content(base, data['__uri__'], **data)
    else:
        return Node(base, data['__uri__'], **data)


class Node(UriObject):
    pass


class Content(Node):

    def update(self, **data):
        status, rec = TRANSPORT.request(
            '%s/%s/update'%(self._base, self.__uri__), params=data)

        if status != 200:
            raise Exception(rec)

        self.__dict__.update(rec)


class Container(Content):

    def create(self, tinfo, name, **data):
        status, rec = TRANSPORT.request(
            '%s/%s/create'%(self._base, self.__uri__),
            {'tinfo': tinfo.__uri__, 'name': name}, data)

        if status != 200:
            raise Exception(rec)

        return createObj(self._base, rec)


class Transport(object):
    """Handles an HTTP transaction to an Ptah server."""

    # client identifier (may be overridden)
    user_agent = "ptahclient.py/%s (by www.ptahproject.org)" % __version__

    #if true, we'll request gzip encoding
    accept_gzip_encoding = True

    def __init__(self, url, token=''):
        r = urlparse.urlparse(url)

        self.h_scheme = r.scheme
        self.h_netloc = r.netloc
        self.h_path = r.path

        self.connection = None
        self.headers = {}
        self.set_auth_token(token)

    def set_auth_token(self, token):
        if token:
            self.headers['X_AUTH_TOKEN'] = token
        elif 'X_AUTH_TOKEN' in self.headers:
            del self.headers['X_AUTH_TOKEN']

    def request(self, handler, args=None, params=None, verbose=0):
        if args:
            handler = '%s?%s'%(handler, urllib.urlencode(args))

        if params:
            request_body = urllib.urlencode(params)
        else:
            request_body = ''
        
        for i in (0, 1):
            try:
                return self.single_request(handler, request_body, verbose)
            except socket.error, e:
                if i or e.errno not in (errno.ECONNRESET,
                                        errno.ECONNABORTED, errno.EPIPE):
                    raise
            except httplib.BadStatusLine: #close after we sent request
                if i:
                    raise

    def single_request(self, handler, request_body, verbose=0):
        h = self.get_connection()
        if verbose:
            h.set_debuglevel(1)

        try:
            headers = dict(self.headers)
            headers['HOST'] = self.h_netloc
            headers['User-Agent'] = self.user_agent
            headers['Content-Type'] = 'application/x-www-form-urlencoded'
            headers['Content-Length'] = len(request_body)
            
            h.request("POST", handler, request_body, headers)
            response = h.getresponse(buffering=True)
            return self.parse_response(response)
        except Exception:
            self.close()
            raise

    def get_connection(self):
        if self.connection:
            return self.connection

        if self.h_scheme == 'https':
            Connection = httplib.HTTPSConnection
        else:
            Connection = httplib.HTTPConnection

        self.connection = Connection(self.h_netloc)
        return self.connection

    def close(self):
        if self.connection:
            self.connection.close()
            self.connection = None

    def send_request(self, connection, handler):
        connection.putrequest(
            "POST", handler, skip_host=True, skip_accept_encoding=True)

    def send_host(self, connection):
        #connection.putheader('HOST', self.h_netloc)

        extra_headers = self.headers
        if extra_headers:
            if isinstance(extra_headers, DictType):
                extra_headers = extra_headers.items()
            for key, value in extra_headers:
                connection.putheader(key, value)

    def send_user_agent(self, connection):
        connection.putheader("User-Agent", self.user_agent)

    def send_content(self, connection, request_body):
        #connection.putheader("Content-Type", "text/plain")
        #connection.putheader("Content-Length", str(len(request_body)))
        connection.endheaders()
        connection.send(request_body)

    def parse_response(self, response):
        p = []
        while 1:
            data = response.read(1024)
            if not data:
                break
            p.append(data)

        return response.status, json.loads(''.join(p))
