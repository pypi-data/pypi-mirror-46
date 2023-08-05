# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['void_object']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'void-object',
    'version': '0.1.3',
    'description': 'Void Object for Python',
    'long_description': "# void-object\nPython Void Object\n\n### Example use case:\n\n```python\nfrom void_object import Void\n\nvoid = Void()\n\nvoid.this_method_does_not_exist()\nvoid.random_attribute\nvoid['asd'][1]\nwith void as ctx:\n    ctx.asd()\n\n```",
    'author': 'Federico Marcos',
    'author_email': 'marcosfede@gmail.com',
    'url': 'https://github.com/marcosfede/void-object',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.4,<4.0',
}


setup(**setup_kwargs)
