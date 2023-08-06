# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['clean_auckland_gtfs']

package_data = \
{'': ['*']}

install_requires = \
['gtfstk>=10,<11']

setup_kwargs = {
    'name': 'clean-auckland-gtfs',
    'version': '0.4.1',
    'description': 'Python 3.6+ code for cleaning Auckland, New Zealand GTFS feeds',
    'long_description': None,
    'author': 'Alex Raichev',
    'author_email': 'araichev@mrcagney.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
