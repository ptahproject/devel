# devapp
import ptah
import transaction
from pyramid.config import Configurator


def includeme(config):
    config.scan()


def main(global_config, **settings):
    """ This is your application startup.
    """
    config = Configurator(settings=settings)
    config.include('pyramid_mailer')
    config.include('ptahcrowd')
    config.include('ptahcms')
    config.include('devapp')

    # init ptah settings
    config.ptah_init_settings()

    # init ptah sqlalchemy
    config.ptah_init_sql()

    # enable rest api
    config.ptah_init_rest()

    # enable ptah manage
    config.ptah_init_manage()

    # enable ptah manage
    config.ptah_populate()

    # set ptah mailer
    from pyramid_mailer.interfaces import IMailer
    mailer = config.registry.queryUtility(IMailer)
    config.ptah_init_mailer(mailer.direct_delivery)

    # We are not in a web request; we need to manually commit.
    transaction.commit()

    return config.make_wsgi_app()
