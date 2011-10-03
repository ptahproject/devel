# devapp

from memphis import view


#view.registerLayout('page', view.INavigationRoot, layer='devapp',
#                    template = view.template('templates/layoutpage.pt'))


view.static('socketio', 'devapp:socketio/')
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
