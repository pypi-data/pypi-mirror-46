import os

from setuptools import setup, find_packages

VERSION = 0.94

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.txt')) as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.txt')) as f:
    CHANGES = f.read()

entry_points = {
    'console_scripts': [
        'app = xxx.scraper.app:main',
        ],
}

requires = [
    'beautifulsoup4',
    'gevent',
    'imagehash',
    'iso8601',
    'pytz',
    'pyyaml',
    'requests',
    'redis',
    'xxx.server-api',
    ]

tests_require = [
    'WebTest >= 1.3.1',  # py3 compat
    'pytest',  # includes virtualenv
    'pytest-cov',
    ]

setup(name='xxx.scraper',
      version=VERSION,
      description='scraper',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
          "Programming Language :: Python",
          "Framework :: Pyramid",
          "Topic :: Internet :: WWW/HTTP",
          "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
      ],
      author='',
      author_email='',
      url='',
      keywords='web',
      packages=find_packages(),
      namespace_packages=['xxx'],
      include_package_data=True,
      zip_safe=False,
      extras_require={
          'testing': tests_require,
      },
      install_requires=requires,
      entry_points=entry_points,
      )
