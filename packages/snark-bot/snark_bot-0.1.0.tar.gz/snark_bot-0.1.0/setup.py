# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['snark_bot']

package_data = \
{'': ['*']}

install_requires = \
['python-dotenv>=0.10.2,<0.11.0',
 'slackclient>=2.0,<3.0',
 'smart-getenv>=1.1,<2.0']

setup_kwargs = {
    'name': 'snark-bot',
    'version': '0.1.0',
    'description': 'Slack bot spewing snarky comments.',
    'long_description': None,
    'author': 'Bram Vereertbrugghen',
    'author_email': 'bram@adimian.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
