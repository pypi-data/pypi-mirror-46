# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['roulier_gls_fr']

package_data = \
{'': ['*']}

install_requires = \
['pycountry>=18.12,<19.0', 'roulier>=0.3.7,<0.4.0']

setup_kwargs = {
    'name': 'roulier-gls-fr',
    'version': '0.1.0',
    'description': 'Send parcels with GLS France delivery carrier. Carrier return parcel label and traceability url',
    'long_description': '',
    'author': 'David Béal',
    'author_email': 'david.beal@akretion.com',
    'url': 'https://github.com/akretion.roulier-gls-fr',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
