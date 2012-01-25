from pyramid.config import Configurator
from pyramid.session import UnencryptedCookieSessionFactoryConfig

from pyramid_sockjs.route import SockJSRoute

session_factory = UnencryptedCookieSessionFactoryConfig('secret')


def main(global_settings, **settings):
    config = Configurator(settings=settings,)
                          #session_factory = session_factory)
    config.include('ptah')
    config.include('ptah_crowd')
    config.include('pyramid_sockjs')

    #config.add_route('views.home', '/')
    config.add_route('views.broadcast', '/broadcast')
    config.scan('devsocket.views')

    config.add_route('views.chat', '/chat.html')
    config.add_view(route_name='views.chat',
                    renderer='devsocket:templates/chat.pt')

    from devsocket.chat import ChatSession

    config.add_sockjs_route(session=ChatSession)

    # init ptah
    config.ptah_init_sql()
    config.ptah_init_settings()

    #config.include('devapp')

    # enable ptah manage
    config.ptah_init_manage(managers=['*'])

    return config.make_wsgi_app()
