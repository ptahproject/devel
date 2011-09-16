from setuptools import setup, find_packages

requires = [
    'ptah',
    'ptah_cms',
    'ptah_app',
    ]

setup(name='devapp',
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
        'memphis': ['package = devapp'],
        },
      )
