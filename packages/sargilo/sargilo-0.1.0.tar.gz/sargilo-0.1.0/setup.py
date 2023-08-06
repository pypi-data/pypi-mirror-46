# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['sargilo',
 'sargilo.integrations',
 'sargilo.tests',
 'sargilo.tests.blog',
 'sargilo.tests.blog.migrations',
 'sargilo.tests.django14_test_project']

package_data = \
{'': ['*'], 'sargilo.tests.django14_test_project': ['templates/*']}

install_requires = \
['ruamel.yaml', 'south']

setup_kwargs = {
    'name': 'sargilo',
    'version': '0.1.0',
    'description': 'Dynamic loader for test data',
    'long_description': None,
    'author': 'Nick Lehmann',
    'author_email': 'nicklehmann@protonmail.ch',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>2.7',
}


setup(**setup_kwargs)
