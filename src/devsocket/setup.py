from setuptools import find_packages
from setuptools import setup


requires = [
    'pyramid',
    'pyramid_socketio',
    'gevent',
    'gevent-socketio',
    'gevent-websocket',
    'greenlet',
]


setup(
    name='devsocket',
    version='0.0',
    description='experimental package',
    classifiers=[
        "Programming Language :: Python",
        "Framework :: Pylons",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
    ],
    packages=find_packages(),
    zip_safe=False,
    install_requires = requires,
    entry_points = {
        'ptah': ['package = devapp'],
        'console_scripts': [
            'socket-server = devsocket.server:main',
        ],
    },
)
