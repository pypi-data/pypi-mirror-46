# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['python_wikibase',
 'python_wikibase.data_model',
 'python_wikibase.data_types',
 'python_wikibase.utils']

package_data = \
{'': ['*']}

install_requires = \
['wikibase-api>=0.1.0,<0.2.0']

setup_kwargs = {
    'name': 'python-wikibase',
    'version': '0.1.0',
    'description': 'Wikibase queries and edits made easy',
    'long_description': '# python-wikibase\n\n**`python-wikibase` provides an object-oriented abstraction of the [Wikibase API](https://www.wikidata.org/w/api.php?action=help).**\n\nThe library simplifies the authentication process and can be used to query and edit information on Wikidata or any other Wikibase instance.\n\n## Example\n\n```py\nfrom python_wikibase import PyWikibase\n\n# Authenticate with Wikibase\npy_wb = PyWikibase(config_path="config.json")\n\n# Fetch item and "coordinate location" property\nitem = py_wb.Item().get(entity_id="item label")\nprop = py_wb.Property().get(entity_id="coordinate location")\n\n# Create new GeoLocation value\nvalue = py_wb.GeoLocation().create(1.23, 4.56)\n\n# Create GeoLocation claim\nclaim = item.claims.add(prop, value)\n```\n\n## Installation\n\n```sh\npip install python-wikibase\n```\n\n## Authentication\n\nThe `PyWikibase` class takes the same authentication and configuration parameters as the `WikibaseApi` class from the [`wikibase-api`](https://github.com/samuelmeuli/wikibase-api) library. See its documentation for a guide on how to authenticate with Wikibase.\n\n## Usage\n\n→ [Documentation](docs/usage.md)\n',
    'author': 'Samuel Meuli',
    'author_email': 'me@samuelmeuli.com',
    'url': 'https://github.com/samuelmeuli/python-wikibase',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
