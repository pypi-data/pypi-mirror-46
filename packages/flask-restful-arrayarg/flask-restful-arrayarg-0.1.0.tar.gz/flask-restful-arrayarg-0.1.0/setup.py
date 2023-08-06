# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['flask_restful_arrayarg']

package_data = \
{'': ['*']}

install_requires = \
['flask-restful>=0.3.7,<0.4.0']

setup_kwargs = {
    'name': 'flask-restful-arrayarg',
    'version': '0.1.0',
    'description': 'An extension to flask-restful argparse for PHP style array forms',
    'long_description': None,
    'author': 'genzj',
    'author_email': 'zj0512@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*',
}


setup(**setup_kwargs)
