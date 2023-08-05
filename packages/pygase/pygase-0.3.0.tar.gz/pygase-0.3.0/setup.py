# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['pygase']

package_data = \
{'': ['*']}

install_requires = \
['curio>=0.9.0,<0.10.0', 'ifaddr>=0.1.6,<0.2.0', 'u-msgpack-python>=2.5,<3.0']

setup_kwargs = {
    'name': 'pygase',
    'version': '0.3.0',
    'description': 'game-ready client-server architecture and UDP-based network protocol - built to be easy to use, lightweight, fast, scalable and reliable',
    'long_description': "[![Build Status](https://dev.azure.com/pxlbrain/pygase/_apis/build/status/sbischoff-ai.pygase?branchName=master)](https://dev.azure.com/pxlbrain/pygase/_build/latest?definitionId=2&branchName=master)\n![Azure DevOps tests (branch)](https://img.shields.io/azure-devops/tests/pxlbrain/pygase/2/master.svg)\n![Azure DevOps coverage (branch)](https://img.shields.io/azure-devops/coverage/pxlbrain/pygase/2/master.svg)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)\n![PyPI](https://img.shields.io/pypi/v/pygase.svg)\n# PyGaSe\n**Py**thon **Ga**me **Se**rver\n\nA package for Python 3.6+ that contains a game-ready client-server architecture and UDP-based network protocol.\n\nIt deals with problems such as package loss or network congestion so you don't have to. Instead it gives you\na high-level API to easily connect clients and backends that share a synchronized game state and exchange events.\nThe async framework for this one is [curio](https://github.com/dabeaz/curio), which I highly recommend.\n\nPyGaSe is built to be easy to use, lightweight, fast, scalable and reliable.\nYou can build a fast-paced real-time online game with this.\nYou can also build a large-scale MMO with thousands of clients if you like.\n\nI'm actively developing PyGaSe in the context of several Indie game projects and I'm happy to share it.\n\n---\n***BREAKING CHANGE**: Version 0.2.0 is basically a new API and updating from 0.1.9 or lower will break you code.*\n*It is also much more stable, flexible and powerful, so make sure to use 0.2.0 or higher.*\n\n---\n\n### Installation\n```\npip install pygase\n```\nor better yet `poetry add pygase`. Seriously, use [poetry](https://github.com/sdispater/poetry), it's a revelation.\n\n## Usage\n\n### API Reference & Tutorials\n\nFor API documentation and a *Getting Started* section go [here](https://sbischoff-ai.github.io/pygase/).\n\n### Example\n\n[This example game](https://github.com/sbischoff-ai/pygase/tree/master/chase) implements an online game of tag,\nin which players can move around, while one of them is the chaser who has to catch another player.\nA player who has been catched becomes the next chaser and can catch other players after a 5s protection countdown.\n\nRun `server.py` first, then run `client.py` in additional terminal sessions to add players.\nOnly use the same player name once.\n\n### Debugging & Logging\n\nYou can use the standard `logging` module. On level `INFO` you will get logging output for events such as\nstartups, shutdowns, new connections or disconnects. On `DEBUG` level you get detailed output right down to the level\nof sending, receiving and handling single network packages.\n\nDebug logs are also a good way to understand the inner workings of PyGaSe.\n\n---\n## Changes\n\n### 0.3.0\n- sticking to SemVer from here on out\n- logging added using the standard `logging` module\n- improve event handler arguments\n- `Backend` class added to reduce server-side boilerplate\n- various bugfixes\n\n### 0.2.0\n- complete overhaul of pygase 0.1.x with breaking API changes\n",
    'author': 'Silas Bischoff',
    'author_email': 'silas.bischoff@googlemail.com',
    'url': 'https://github.com/sbischoff-ai/python-game-service',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
