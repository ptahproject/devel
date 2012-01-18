import ptah
from pyramid.testing import DummyRequest
from pyramid.httpexceptions import HTTPNotFound, HTTPForbidden


class TestExceptions(ptah.PtahTestCase):

    def tearDown(self):
        config.cleanup_system(self.__class__.__module__)
        super(TestExceptions, self).tearDown()

    def test_not_found(self):
        from devapp.exc import NotFound
        self._init_ptah()

        class Context(object):
            """ """

        request = DummyRequest()
        request.root = Context()

        excview = NotFound(HTTPNotFound(), request)
        excview.update()

        self.assertIs(excview.__parent__, request.root)
        self.assertEqual(request.response.status, '404 Not Found')
