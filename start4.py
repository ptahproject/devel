""" Demonstrate an empty non-bootstrapped Ptah CMS.
    The goal of this is to exercise removing Ptah App from runtime.
    You will have to do *everything* yourself.
"""
from paste.httpserver import serve
import memphis
import transaction
import pyramid_sqla
from pyramid import path
from pyramid.config import Configurator

import ptah

def make_app(global_config, **settings):
    """ ripped from ptah/__init__.py:initializeSettings """

    config = Configurator(settings=settings)
    try:
        # This is magic land.
        # intializing invokes a memphis scan of PYTHONPATH
        # What I really want is to 
        ptah.initialize(None, config, global_config)
    except memphis.config.StopException:
        memphis.config.shutdown()
        raise

    # Pyramid
    app = config.make_wsgi_app()

    Base = pyramid_sqla.get_base()
    Base.metadata.create_all()

    config.begin()

    # Memphis, send ApplicationStarting event
    memphis.config.start(config)

    # Ptah, app initialized
    config.registry.notify(ptah.AppInitialized(app, config))

    config.end()
    config.commit()

    # commit possible transaction
    transaction.commit()

    return app

def main(global_config):
    app = make_app(global_config)
    return app

""" In PYTHONPATH we have quite a few modules which have memphis entry points.
    What we will do now, for cheapness, is just exclude the packages which
    define behaviors for Ptah.  In the future we can have a nicer example.

    Starting this and going to http://localhost:8080/ you get 404.  There is
    no ptah_app, we excluded it.  What is left is Ptah Manage, which is in
    the core Ptah package. http://localhost:8080/ptah-manage/ you can even
    remove Ptah Manage.  But for now this environment will work fine for
    demonstration purposes.
 
"""

if __name__ == '__main__':
    app = main({'settings':'./ptah.ini',
                'excludes':'ptah_app devapp devpoll'})
    serve(app, '0.0.0.0')

