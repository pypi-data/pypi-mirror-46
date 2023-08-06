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
    'version': '0.1.1',
    'description': 'Wrapper library for the Wikibase API',
    'long_description': '# wikibase-api\n\n`wikibase-api` is a Python library for simple access to the [Wikibase API](https://www.wikidata.org/w/api.php?action=help). It simplifies the authentication process and can be used to query and edit information on Wikidata or any other Wikibase instance.\n\nFor an simpler, object-oriented abstraction of the Wikibase API, have a look at [`python-wikibase`](https://github.com/samuelmeuli/python-wikibase).\n\n## Installation\n\n```sh\npip install wikibase-api\n```\n\n## Usage\n\nSimple example for getting all information about a Wikidata page:\n\n```python\nfrom wikibase_api import Wikibase\n\nwb = Wikibase()\nr = wb.entity.get("Q1")\nprint(r)\n```\n\nOutput:\n\n```python\n{\n  "entities": {\n    "Q1": {\n      # ...\n    }\n  },\n  "success": 1,\n}\n```\n\n## Documentation\n\n→ **[Docs](https://wikibase-api.readthedocs.io)**\n\nThe documentation for this library can be built using the following commands (you\'ll need to have Python, Make and [Poetry](https://poetry.eustace.io) installed):\n\n```sh\ngit clone REPO_URL\nmake install\nmake docs-build\nmake docs-open\n```\n',
    'author': 'Samuel Meuli',
    'author_email': 'me@samuelmeuli.com',
    'url': 'https://github.com/samuelmeuli/wikibase-api',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
