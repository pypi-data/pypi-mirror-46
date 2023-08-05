# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['terminology']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'terminology',
    'version': '1.0.5',
    'description': 'An intuitive way to color terminal text',
    'long_description': '',
    'author': 'Juan Gonzalez',
    'author_email': 'jrg2156@gmail.com',
    'url': 'https://github.com/juanrgon/terminology',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=2',
}


setup(**setup_kwargs)
