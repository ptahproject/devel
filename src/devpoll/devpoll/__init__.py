# devpoll
from ptah import view

import app

view.register_route(
    'devpoll-poll-view', '/polls/{id}/',
    app.pollAppFactory)


view.register_route(
    'devpoll-application', '/polls/*traverse',
    app.pollAppFactory, use_global_views = True)


def pre_install(cfg):
    from devpoll.poll import Poll
    if not Poll.__table__.exists():
        Poll.__table__.create()


def post_install():
    pass


def pre_uninstall():
    pass


def post_uninstall():
    pass
