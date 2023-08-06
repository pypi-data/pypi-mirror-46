# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['electricitycostcalculator_gabetest',
 'electricitycostcalculator_gabetest.cost_calculator',
 'electricitycostcalculator_gabetest.oadr_signal',
 'electricitycostcalculator_gabetest.openei_tariff']

package_data = \
{'': ['*']}

install_requires = \
['holidays>=0.9.10,<0.10.0',
 'lxml>=4.3,<5.0',
 'matplotlib>=3.0,<4.0',
 'pandas>=0.24.2,<0.25.0',
 'pytz>=2019.1,<2020.0',
 'requests>=2.21,<3.0']

setup_kwargs = {
    'name': 'electricitycostcalculator-gabetest',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'Olivier Van Cutsem',
    'author_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
