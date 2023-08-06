# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['pugsql']

package_data = \
{'': ['*']}

install_requires = \
['sqlalchemy>=1.3,<2.0']

setup_kwargs = {
    'name': 'pugsql',
    'version': '0.1.2',
    'description': '',
    'long_description': None,
    'author': 'Dan McKinley',
    'author_email': 'mcfunley@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
