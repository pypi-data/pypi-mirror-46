# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['lamon', 'lamon.views', 'lamon.watcher', 'lamon.watcher.plugin']

package_data = \
{'': ['*'],
 'lamon': ['static/bootstrap/css/*',
           'static/bootstrap/js/*',
           'static/css/*',
           'templates/*',
           'templates/game/*',
           'templates/main/*',
           'templates/user/*',
           'templates/watcher/*']}

install_requires = \
['flask-admin>=1.5,<2.0',
 'flask-sqlalchemy>=2.3,<3.0',
 'flask-user==0.6.21',
 'flask-wtf>=0.14.2,<0.15.0',
 'flask>=1.0,<2.0',
 'jinja2>=2.10,<3.0',
 'python-valve>=0.2.1,<0.3.0',
 'sqlalchemy>=1.2,<2.0',
 'toml>=0.10.0,<0.11.0']

setup_kwargs = {
    'name': 'lamon',
    'version': '0.1.0',
    'description': 'Monitor gameservers',
    'long_description': None,
    'author': 'Fabian Geiselhart',
    'author_email': 'me@f4814n.de',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
