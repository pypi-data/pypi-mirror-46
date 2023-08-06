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
    'version': '0.1.5',
    'description': 'PugSQL is an anti-ORM that facilitates interacting with databases using SQL in files.',
    'long_description': None,
    'author': 'Dan McKinley',
    'author_email': 'mcfunley@gmail.com',
    'url': 'https://pugsql.org',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.4',
}


setup(**setup_kwargs)
