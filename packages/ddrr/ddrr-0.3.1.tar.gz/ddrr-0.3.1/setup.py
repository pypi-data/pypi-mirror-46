# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['ddrr', 'ddrr.templatetags']

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
    'version': '0.3.1',
    'description': '',
    'long_description': '# Django Debug Requests & Responses (DDRR)\n\nGet more out of your `runserver` development output! Print request and response\nheaders, body (with pretty-printing), etc.  Highly customizable!\n\n- Full request headers\n- The entire request body\n- Pretty-printing optional\n- Colored output\n- Super easy setup\n- No extra dependencies\n\nDDRR can also be used for general logging with some configuration of your own.\n\n## Installation\n\n```\n$ pip install ddrr\n```\n\n```python\n# in settings.py\nINSTALLED_APPS = (\n    # ...\n    "ddrr",\n)\n\nimport ddrr\nddrr.quick_setup()\n```\n\n**Done!** When you run `runserver`, you\'ll now get the entire HTTP requests and\nresponses, including headers and bodies.\n\nIf you don\'t like the default output format, read on...\n\n### Customization\n\n`ddrr.quick_setup` accepts the following optional arguments:\n\n- `enable_requests` - (default: True) Enable request logging.\n- `enable_responses` - (default: True) Enable response logging.\n- `level` - (default: DEBUG) The level of the log messages.\n- `pretty` - (default: False) Enable pretty-printing of bodies.\n- `request_template` - (default: None) Request template string\n- `request_template_name` - (default: None) Request template name\n- `response_template` - (default: None) Response template string\n- `response_template_name` - (default: None) Response template name\n- `limit_body` - (default: None) Limit request and response body length\n- `colors` - (default: True) Enable color support if terminal supports it\n\n### Change output formats\n\nYou can pass `request_template` or `request_template_name` to `quick_setup` to\ndefine a different output format for request logs. The same goes for responses,\nuse `response_template` or `response_template_name`.\n\nThe templates are normal Django templates which are passed the necessary\ntemplate context with access to pretty much anything you could be interested in.\n\n- **Request template context:**\n  - `ddrr.body` - request body\n  - `ddrr.content_type` - request content type\n  - `ddrr.formatter` - the formatter\n  - `ddrr.headers` - mapping of header fields and values\n  - `ddrr.method` - request method\n  - `ddrr.path` - request path\n  - `ddrr.query_params` - query parameters\n  - `ddrr.query_string` - query string\n  - `ddrr.record` - the actual log record object\n  - `ddrr.request` - the actual request object\n- **Response template context:**\n  - `ddrr.content` - response content\n  - `ddrr.content_type` - response content type\n  - `ddrr.formatter` - the formatter\n  - `ddrr.headers` - mapping of header fields and values\n  - `ddrr.reason_phrase` - response reason phrase\n  - `ddrr.record` - the actual log record object\n  - `ddrr.response` - the actual response object\n  - `ddrr.status_code` - response status code\n\nFor example, this will log the method, path and body of each request, as well\nas the status code, reason phrase and content of each response:\n\n```python\nddrr.quick_setup(\n    request_template="{{ ddrr.method }} {{ ddrr.path }}\\n"\n                     "{{ ddrr.body }}",\n    response_template="{{ ddrr.status_code }} {{ ddrr.reason_phrase }}\\n"\n                      "{{ ddrr.content }}",\n)\n```\n\n### Pretty-printing\n\nBy default, pretty-printing is disabled. Pass `pretty=True` to `quick_setup` to\nenable it.\n\nPretty-printing of JSON requires not external dependency.\n\nPretty-printing of XML uses `minidom` by default and doesn\'t require any extra\ndependency. If you want to use `lxml` instead, which is slightly better at\npretty-printing XML, you can install that using `pip install ddrr[xml]`.\n\n### How it works internally\n\nThe middleware `ddrr.middleware.DebugRequestsResponses` sends the entire\nrequest object as the message to `ddrr-request-logger`.  This logger has been\nconfigured to use `ddrr.formatters.DjangoTemplateRequestFormatter` which\ninternally uses Django\'s built-in template engine to format the request into\nhuman-readable form. By default, this is shown in your console output, but you\ncan easily configure it to log it to a file, ElasticSearch, or anything else.\n\n## Similar projects\n\n- [Django Debug Toolbar](https://django-debug-toolbar.readthedocs.io)\n\n## Development and contributions\n\nPR\'s are always welcome!\n\nFor hacking on DDRR, make sure you are familiar with:\n\n- [Black](https://github.com/ambv/black)\n- [Flake8](http://flake8.pycqa.org/)\n- [Poetry](https://poetry.eustace.io/)\n- [pre-commit](https://github.com/pre-commit/pre-commit)\n- [pytest](https://docs.pytest.org)\n\nInstall dependencies and set up the pre-commit hooks.\n\n```\n$ poetry install\n$ pre-commit install\n```\n\nThe pre-commit hooks will, among other things, run Flake8 on the code base and\nBlack to make sure the code style is consistent across all files.  Check out\n[`.pre-commit-config.yaml`](.pre-commit-config.yaml) for details.\n',
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
