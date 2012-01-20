from pyramid.config import Configurator
from pyramid.session import UnencryptedCookieSessionFactoryConfig

session_factory = UnencryptedCookieSessionFactoryConfig('secret')


def main(global_settings, **settings):
    config = Configurator(settings=settings,)
                          #session_factory = session_factory)
    config.include('ptah')

    config.add_route('views.home', '/')
    config.add_route('views.broadcast', '/broadcast')
    config.scan('devsocket.views')

    # init ptah settings
    config.ptah_init_settings()

    # enable ptah manage
    config.ptah_init_manage(managers=['*'])

    return config.make_wsgi_app()
