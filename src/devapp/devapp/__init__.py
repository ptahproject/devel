# devapp
import sqlahelper
import transaction
from pyramid.config import Configurator


def includeme(config):
    config.scan()


def main(global_config, **settings):
    """ This is your application startup.
    """
    config = Configurator(settings=settings)
    config.commit()
    config.begin()

    # init ptah
    config.ptah_initialize()

    # enable rest api
    config.ptah_rest_api()

    # create sql tables
    Base = sqlahelper.get_base()
    Base.metadata.create_all()

    # We are not in a web request; we need to manually commit.
    transaction.commit()

    return config.make_wsgi_app()
