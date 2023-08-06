# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['wikibase_api', 'wikibase_api.models']

package_data = \
{'': ['*'], 'wikibase_api': ['utils/*']}

install_requires = \
['requests-oauthlib>=1.0,<2.0', 'requests>=2.20,<3.0']

setup_kwargs = {
    'name': 'wikibase-api',
    'version': '0.1.0',
    'description': 'Wrapper library for the Wikibase API',
    'long_description': None,
    'author': 'Samuel Meuli',
    'author_email': 'me@samuelmeuli.com',
    'url': 'https://github.com/samuelmeuli/wikibase-api',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
