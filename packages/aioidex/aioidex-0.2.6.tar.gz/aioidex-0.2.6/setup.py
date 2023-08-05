# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['aioidex', 'aioidex.datastream', 'aioidex.http', 'aioidex.tests']

package_data = \
{'': ['*'], 'aioidex': ['types/*'], 'aioidex.http': ['modules/*']}

install_requires = \
['aiohttp>=3.5,<4.0',
 'backoff>=1.8,<2.0',
 'shortid>=0.1.2,<0.2.0',
 'ujson>=1.35,<2.0',
 'websockets>=7.0,<8.0']

setup_kwargs = {
    'name': 'aioidex',
    'version': '0.2.6',
    'description': 'Idex API async Python wrapper',
    'long_description': None,
    'author': 'ape364',
    'author_email': 'ape364@gmail.com',
    'url': 'https://github.com/ape364/aioidex',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
