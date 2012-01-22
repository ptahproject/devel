from setuptools import setup, find_packages


requires = [
    'pyramid',
    'pyramid_sockjs',
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
        'paste.app_factory': [
            'main = devsocket.app:main'],
        },
    )
