# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['ddrr']

package_data = \
{'': ['*'], 'ddrr': ['templates/ddrr/*']}

install_requires = \
['attrs>=19.1,<20.0']

extras_require = \
{':python_version >= "2.7" and python_version < "2.8"': ['Django>=1.11,<2.0'],
 ':python_version >= "3.5" and python_version < "4.0"': ['Django>=2.0,<3.0'],
 'xml': ['lxml>=4.3,<5.0']}

setup_kwargs = {
    'name': 'ddrr',
    'version': '0.2.0',
    'description': '',
    'long_description': '# Django Debug Requests & Responses (DDRR)\n\nGet more out of your `runserver` development output! Print request and response\nheaders, body (with pretty-printing), etc.  Highly customizable!\n\n- Log request headers\n- Log request body\n- Pretty-print JSON request and response bodies\n- ...and more!\n\nDDRR can also be used for general logging with some configuration of your own.\n\n## Installation\n\n```\n$ pip install ddrr\n```\n\n1. Add `ddrr` to your `INSTALLED_APPS`:\n\n    ```python\n    # in settings.py\n    INSTALLED_APPS = (\n        # ...\n        "ddrr",\n    )\n    ```\n\n1. Configure the logging of your Django app to use DDRR:\n\n    ```python\n    # in settings.py\n    import ddrr\n    ddrr.quick_setup()\n    ```\n\n1. **Done!**\n\n## Customization\n\n### Change output formats\n\nTODO\n\n## How it works\n\nThe middleware `ddrr.middleware.DebugRequestsResponses` sends the entire\nrequest object as the message to `ddrr-request-logger`.  This logger has been\nconfigured to use `ddrr.formatters.DefaultRequestFormatter` which internally\nuses Django\'s built-in template engine to format the request into human-readable\nform. By default, this is shown in your console output, but you can easily\nconfigure it to log it to a file, ElasticSearch, or anything else.\n\n## Similar projects\n\n- [Django Debug Toolbar](https://django-debug-toolbar.readthedocs.io)\n\n## Development and contributions\n\nPR\'s are always welcome!\n\nFor hacking on DDRR, make sure you are familiar with:\n\n- [Black](https://github.com/ambv/black)\n- [Flake8](http://flake8.pycqa.org/)\n- [Poetry](https://poetry.eustace.io/)\n- [pre-commit](https://github.com/pre-commit/pre-commit)\n- [pytest](https://docs.pytest.org)\n\nInstall dependencies and set up the pre-commit hooks.\n\n```\n$ poetry install\n$ pre-commit install\n```\n\nThe pre-commit hooks will, among other things, run Flake8 on the code base and\nBlack to make sure the code style is consistent across all files.  Check out\n[`.pre-commit-config.yaml`](.pre-commit-config.yaml) for details.\n',
    'author': 'Deniz Dogan',
    'author_email': 'denizdogan@users.noreply.github.com',
    'url': 'https://github.com/denizdogan/django-debug-requests-responses',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*',
}


setup(**setup_kwargs)
