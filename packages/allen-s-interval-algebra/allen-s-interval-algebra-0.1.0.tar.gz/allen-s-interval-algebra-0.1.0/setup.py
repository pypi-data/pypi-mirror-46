# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['allen_s_interval_algebra']

package_data = \
{'': ['*']}

install_requires = \
['pytz>=2019.1,<2020.0']

setup_kwargs = {
    'name': 'allen-s-interval-algebra',
    'version': '0.1.0',
    'description': "Implementation of the Allen's interval algebra",
    'long_description': None,
    'author': 'Tanguy Le Carrour',
    'author_email': 'tanguy@bioneland.org',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
