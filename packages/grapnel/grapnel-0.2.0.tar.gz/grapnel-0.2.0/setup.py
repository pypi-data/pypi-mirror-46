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
    'version': '0.2.0',
    'description': 'Add hooks to your python classes.',
    'long_description': 'Grapnel\n=======\n\nGrapnel is a library that provides Python classes with Hooks. Hooks allow other parts of the codebase to register functions or methods as callbacks. When a Hook is triggered by an instance of the class, the callbacks are invoked.\n',
    'author': 'artPlusPlus',
    'author_email': 'artPlusPlus@users.noreply.github.com',
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
