# tartaroo
from memphis import view

import app

view.registerRoute(
    'devpoll-poll-view', '/polls/{id}/',
    app.pollAppFactory)

view.registerRoute(
    'devpoll-application', '/polls/*traverse',
    app.pollAppFactory, use_global_views = True)
