# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['trackside']

package_data = \
{'': ['*'], 'trackside': ['data/*']}

install_requires = \
['configparser>=5.2.0,<6.0.0', 'influxdb>=5.3.1,<6.0.0', 'pyserial>=3.5,<4.0']

setup_kwargs = {
    'name': 'trackside',
    'version': '0.9.0',
    'description': 'Trackside Telemetry for Gopher Motorsports',
    'long_description': None,
    'author': 'Anton King',
    'author_email': 'https://github.com/antonsking',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
