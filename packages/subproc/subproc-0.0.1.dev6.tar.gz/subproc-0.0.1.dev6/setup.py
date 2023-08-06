# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['subproc']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'subproc',
    'version': '0.0.1.dev6',
    'description': 'Provides utility functions around subprocess module.',
    'long_description': None,
    'author': 'Mustafa Caylak',
    'author_email': 'mustafa.caylak@web.de',
    'url': None,
    'packages': packages,
    'package_data': package_data,
}


setup(**setup_kwargs)
