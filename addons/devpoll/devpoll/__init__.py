# devpoll
from ptah import view

import app

view.register_route(
    'devpoll-poll-view', '/polls/{id}/',
    app.pollAppFactory)

view.register_route(
    'devpoll-application', '/polls/*traverse',
    app.pollAppFactory, use_global_views = True)
