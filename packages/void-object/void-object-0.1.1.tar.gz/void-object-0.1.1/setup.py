# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['void_object']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'void-object',
    'version': '0.1.1',
    'description': 'Void Object for Python',
    'long_description': None,
    'author': 'Federico Marcos',
    'author_email': 'marcosfede@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.4',
}


setup(**setup_kwargs)
