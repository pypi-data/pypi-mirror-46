# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['circlecitest']

package_data = \
{'': ['*'], 'circlecitest': ['tests/*']}

install_requires = \
['aiohttp>=3.5,<4.0']

setup_kwargs = {
    'name': 'circlecitest',
    'version': '0.1.0',
    'description': 'testing pypi deploy',
    'long_description': None,
    'author': 'ape364',
    'author_email': 'ape364@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
