# -*- coding: utf-8 -*-
from distutils.core import setup

package_dir = \
{'': 'src'}

packages = \
['buvar']

package_data = \
{'': ['*']}

install_requires = \
['attrs', 'pytoml', 'structlog']

setup_kwargs = {
    'name': 'buvar',
    'version': '0.5.0',
    'description': 'General purpose config loader',
    'long_description': None,
    'author': 'Oliver Berger',
    'author_email': 'diefans@gmail.com',
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
