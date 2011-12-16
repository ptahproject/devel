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
    config.include('ptah_crowd')
    config.commit()
    config.begin()

    # init ptah settings
    config.ptah_initialize_settings()

    # init ptah sqlalchemy
    config.ptah_initialize_sql()

    # enable rest api
    config.ptah_rest_api()

    # enable ptah manage
    config.ptah_manage()

    # create sql tables
    Base = ptah.get_base()
    Base.metadata.create_all()

    # We are not in a web request; we need to manually commit.
    transaction.commit()

    return config.make_wsgi_app()
