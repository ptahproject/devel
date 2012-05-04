from setuptools import find_packages
from setuptools import setup


requires = [
    'ptah',
    'ptahcms',
    'ptahcrowd',
    'poster',
    'pyramid_beaker',
    'pyramid_mailer',
]


setup(
    name='devapp',
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
        'paste.app_factory': [
            'main = devapp:main'],
    },
)
