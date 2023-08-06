# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['sbot']

package_data = \
{'': ['*']}

install_requires = \
['j5>=0.4.0,<0.5.0']

setup_kwargs = {
    'name': 'sbot',
    'version': '0.2.0',
    'description': 'Experimental SourceBots API',
    'long_description': "# sbot\n\n`sbot` - SourceBots Robot API - Powered by j5\n\nThis is an experimental API for SourceBots, based on the [j5](https://github.com/j5api/j5)\nlibrary for writing Robotics APIs. If successful, it could potentially be deployed at\nSourceBots / Smallpeice 2019.\n\nMuch like it's predecessor, [robot-api](https://github.com/sourcebots/robot-api), `sbot` supports\nmultiple backends, although should be more reliable as there is no `UNIX-AF` socket layer.\n\n## Installation\n\nOnce published:\n\nInstall: `pip install sbot`\n\n## Usage\n\n```python\n\nfrom sbot import Robot\n\nr = Robot()\n\n```\n\nOr alternatively:\n\n```python\n\nfrom sbot import Robot\n\nr = Robot(wait_start=False)\n\n# Setup in here\n\nr.wait_start()\n\n```",
    'author': 'Dan Trickey',
    'author_email': 'dan@trickey.io',
    'url': 'https://sourcebots.co.uk',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
