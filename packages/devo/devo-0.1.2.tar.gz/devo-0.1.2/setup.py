# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['devo', 'devo.kube']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.0,<8.0']

entry_points = \
{'console_scripts': ['devo = devo.main:cli']}

setup_kwargs = {
    'name': 'devo',
    'version': '0.1.2',
    'description': '',
    'long_description': None,
    'author': 'Dominic Werner',
    'author_email': 'aka.vince@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
