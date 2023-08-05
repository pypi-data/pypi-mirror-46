# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['terminology']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'terminology',
    'version': '0.1.0',
    'description': 'An intuitive way to create fancy terminal output',
    'long_description': None,
    'author': 'Juan Gonzalez',
    'author_email': 'jrg2156@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
