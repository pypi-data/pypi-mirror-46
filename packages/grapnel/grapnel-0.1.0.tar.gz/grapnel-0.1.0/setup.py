# -*- coding: utf-8 -*-
from distutils.core import setup

package_dir = \
{'': 'src'}

packages = \
['grapnel']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'grapnel',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'artPlusPlus',
    'author_email': 'artPlusPlus@users.noreply.github.com',
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
