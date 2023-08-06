# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['gym_holdem', 'gym_holdem.envs', 'gym_holdem.holdem']

package_data = \
{'': ['*']}

install_requires = \
['gym>=0.12.1,<0.13.0',
 'pokereval-cactus>=0.1.0,<0.2.0',
 'pytest-azurepipelines>=0.6.0,<0.7.0',
 'pytest>=4.5,<5.0']

setup_kwargs = {
    'name': 'gym-holdem',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'Jan Adä',
    'author_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
