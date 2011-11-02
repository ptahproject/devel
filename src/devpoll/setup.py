from setuptools import find_packages
from setuptools import setup

requires = [
    'ptah',
]

setup(
    name='devpoll',
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
        'ptah': ['addon = devpoll',
                 'pre_install = devpoll:pre_install',
                 'post_install = devpoll:post_install',
                 'pre_uninstall = devpoll:pre_uninstall',
                 'post_uninstall = devpoll:post_uninstall',
                 ],
    },
)
