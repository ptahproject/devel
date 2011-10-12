# devapp

import ptah_app
import ptah_app.views

from memphis import view


view.registerLayout('page', ptah_cms.ApplicationRoot, layer='devapp',
                    template = view.template('templates/layoutpage.pt'))

view.registerLayout('page', view.INavigationRoot, layer='devapp',
                    template = view.template('templates/layoutpage.pt'))


view.static('socketio', 'devsocket:socketio/')
view.library(
    'socket.io',
    path="socket.io.js",
    resource="socketio",
    type="js",
    require='jquery',
)
view.library(
    'sticky.min.css',
    path="sticky.min.css",
    resource="socketio",
    type="css",
)
view.library(
    'sticky.min.js',
    path="sticky.min.js",
    resource="socketio",
    type="js",
    require='jquery',
)
