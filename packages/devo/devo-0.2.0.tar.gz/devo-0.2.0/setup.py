# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['devo',
 'devo.build',
 'devo.create',
 'devo.delete',
 'devo.deploy',
 'devo.dev',
 'devo.kube']

package_data = \
{'': ['*'],
 'devo': ['templates/k8s/*',
          'templates/k8s/base/*',
          'templates/project/*',
          'templates/project/{{cookiecutter.project_name}}/*',
          'templates/project/{{cookiecutter.project_name}}/requirements/*',
          'templates/project/{{cookiecutter.project_name}}/scripts/*',
          'templates/project/{{cookiecutter.project_name}}/tests/*',
          'templates/project/{{cookiecutter.project_name}}/{{cookiecutter.project_name}}/*']}

install_requires = \
['click>=7.0,<8.0',
 'cookiecutter>=1.6.0,<2.0.0',
 'ruamel.yaml>=0.15.94,<0.16.0']

entry_points = \
{'console_scripts': ['devo = devo.main:cli']}

setup_kwargs = {
    'name': 'devo',
    'version': '0.2.0',
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
