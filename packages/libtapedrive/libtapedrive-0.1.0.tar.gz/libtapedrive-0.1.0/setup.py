# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['libtapedrive', 'libtapedrive.parsers']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.7,<5.0',
 'bleach>=3.1,<4.0',
 'enlighten>=1.3,<2.0',
 'feedparser>=5.2,<6.0',
 'html5lib>=1.0,<2.0',
 'pillow>=6.0,<7.0',
 'python-dateutil>=2.8,<3.0',
 'requests>=2.21,<3.0']

setup_kwargs = {
    'name': 'libtapedrive',
    'version': '0.1.0',
    'description': 'Podcast client library for feed parsing',
    'long_description': '# libtapedrive — Podcast client library for feed parsing\n\nFundamental component of [Tape Drive](https://tapedrive.io).\n\n[![pipeline status](https://gitlab.com/janw/libtapedrive/badges/master/pipeline.svg)](https://gitlab.com/janw/libtapedrive/commits/master)\n[![coverage report](https://gitlab.com/janw/libtapedrive/badges/master/coverage.svg)](https://gitlab.com/janw/libtapedrive/commits/master)\n[![Maintainability](https://api.codeclimate.com/v1/badges/2a6bf1b4ed42e2c490b8/maintainability)](https://codeclimate.com/github/janw/libtapedrive/maintainability)\n\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/python/black)\n[![Dependency management: poetry](https://img.shields.io/badge/deps-poetry-blueviolet.svg)](https://poetry.eustace.io/docs/)\n![PyPI - Status](https://img.shields.io/pypi/status/libtapedrive.svg)\n![PyPI](https://img.shields.io/pypi/v/libtapedrive.svg)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/libtapedrive.svg)\n',
    'author': 'Jan Willhaus',
    'author_email': 'mail@janwillhaus.de',
    'url': 'https://tapedrive.io',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
