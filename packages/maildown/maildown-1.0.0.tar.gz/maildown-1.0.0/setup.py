# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['maildown']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.9,<2.0',
 'cleo>=0.7.2,<0.8.0',
 'jinja2>=2.10,<3.0',
 'mistune>=0.8.4,<0.9.0',
 'pygments>=2.3,<3.0',
 'requests>=2.21,<3.0',
 'toml>=0.10.0,<0.11.0']

entry_points = \
{'console_scripts': ['maildown = maildown-cli:run']}

setup_kwargs = {
    'name': 'maildown',
    'version': '1.0.0',
    'description': 'A super simple CLI for sending emails',
    'long_description': '# Maildown\n\nA super simple CLI for sending emails\n\n',
    'author': 'Christopher Davies',
    'author_email': 'christopherdavies553@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
