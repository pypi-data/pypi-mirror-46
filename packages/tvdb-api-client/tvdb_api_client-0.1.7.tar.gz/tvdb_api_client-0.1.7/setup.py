# -*- coding: utf-8 -*-
from distutils.core import setup

package_dir = \
{'': 'src'}

packages = \
['tvdb_api_client']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.0,<3.0']

setup_kwargs = {
    'name': 'tvdb-api-client',
    'version': '0.1.7',
    'description': 'A python client for TVDB rest API',
    'long_description': 'This project is a python client for the TVDB API.\n',
    'author': 'spapanik',
    'author_email': 'spapanik21@gmail.com',
    'url': 'https://github.com/spapanik/tvdb_api_client',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
