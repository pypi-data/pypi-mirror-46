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
    'version': '0.2.0',
    'description': 'A python client for TVDB rest API',
    'long_description': '<p align="center">\n    <a href="https://github.com/ambv/black">\n        <img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg">\n    </a>\n</p>\n\nA python client for the <a href="https://api.thetvdb.com/swagger#/">API</a> exposed by <a href="https://api.thetvdb.com/swagger#/">the TVDB</a>. API keys should be acquired from the TVDB site prior to using this client.\n\n### Installation\n\ntvdb_api_client can be installed by running `pip install tvdb_api_client`.  It requires Python 3.6+.\n\n### Usage\n\nInitialise the client (example using the django cache):\n```python\nfrom django.core.cache import cache\nfrom tvdb_api_client import TVDBClient\n\nclient = TVDBClient("username", "user_key", "api_key", cache)\n```\n\nThe cache can be any object from a class that implements the get and set methods. The simplest solution would be the following:\n```python\nclass C(dict):\n    def set(self, key, value):\n        self[key] = value\n\ncache = C()\n```\n\nIt is advisable to use a cache that will persist during a server restart, so that the token will not have to be regenerated. Please be advised that the token will be stored in the cache in plaintext, so if there are any security considerations they should be taken care into account when choosing the cache.\n\nOnce the client has been initialised, you can use it to get the following info (and the respective methods):\n\n- Method to get TV series by TVDB id - `get_series_by_id(tvdb_id)`\n- Method to get TV series by IMDb id - `get_series_by_imdb_id(imdb_id)`\n- Method to find identifying info for a TV series by its name - `find_series_by_name(series_name)`\n- Method to get episodes by TV series using its TVDB id - `get_episodes_by_series(tvdb_id)`\n\nNote: the TVDB id can be an integer of a string in any method that it\'s required.\n',
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
