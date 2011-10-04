import gevent.monkey

import gevent
import socketio

from pyramid.config import Configurator


HOST = '0.0.0.0'
PORT = 9090


def make_app(**settings):
    config = Configurator(settings=settings)
    config.add_route('views.home', '/')
    config.add_route('views.broadcast', '/broadcast')
    config.add_route('views.socket_io', '/socket.io/*remaining')
    config.scan('devsocket.views')
    app = config.make_wsgi_app()
    return app


def serve_gevent(app, host=HOST, port=PORT):
    server = socketio.SocketIOServer((host, port), app, resource='socket.io')
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.kill()


def spawned_main():
    settings = {}
    app = make_app(**settings)
    serve_gevent(app)


def main():
    jobs = [gevent.spawn(spawned_main)]
    gevent.joinall(jobs)


if __name__ == '__main__':
    gevent.monkey.patch_all()
    main()
