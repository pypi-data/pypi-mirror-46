# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['ddrr']

package_data = \
{'': ['*'], 'ddrr': ['templates/ddrr/*']}

install_requires = \
['attrs>=19.1,<20.0', 'lxml[xml]>=4.3,<5.0']

extras_require = \
{':python_version >= "2.7" and python_version < "2.8"': ['Django>=1.11,<2.0'],
 ':python_version >= "3.5" and python_version < "4.0"': ['Django>=2.0,<3.0']}

setup_kwargs = {
    'name': 'ddrr',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Deniz Dogan',
    'author_email': 'denizdogan@users.noreply.github.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*',
}


setup(**setup_kwargs)
