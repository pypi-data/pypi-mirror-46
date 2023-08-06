# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['slack', 'slack.io', 'slack.tests', 'slack.tests.data']

package_data = \
{'': ['*']}

extras_require = \
{'aiohttp': ['aiohttp>=3.4,<4.0'],
 'curio': ['curio>=0.9.0,<0.10.0', 'asks>=2.2,<3.0'],
 'requests': ['requests>=2.20,<3.0', 'websocket-client>=0.54.0,<0.55.0'],
 'trio': ['asks>=2.2,<3.0', 'trio>=0.9.0,<0.10.0']}

setup_kwargs = {
    'name': 'slack-sansio',
    'version': '1.0.0',
    'description': 'Python (a)sync Slack API library',
    'long_description': None,
    'author': 'Ovv',
    'author_email': 'contact@ovv.wtf',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
