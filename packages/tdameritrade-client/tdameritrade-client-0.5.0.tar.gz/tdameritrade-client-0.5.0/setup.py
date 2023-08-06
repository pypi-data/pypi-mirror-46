# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['tdameritrade_client', 'tdameritrade_client.utils']

package_data = \
{'': ['*']}

install_requires = \
['environs>=4.1,<5.0', 'pyopenssl>=19.0,<20.0', 'requests>=2.21,<3.0']

setup_kwargs = {
    'name': 'tdameritrade-client',
    'version': '0.5.0',
    'description': 'A client for the TDA API',
    'long_description': '[![Pipeline Status](https://gitlab.com/tdameritrade-tools/tdameritrade-client/badges/master/pipeline.svg)](https://gitlab.com/tdameritrade-tools/tdameritrade-client/commits/master) [![Documentation Status](https://readthedocs.org/projects/tdameritrade-client/badge/?version=latest)](https://tdameritrade-client.readthedocs.io/en/latest/?badge=latest) [![Coverage Report](https://gitlab.com/tdameritrade-tools/tdameritrade-client/badges/master/coverage.svg)](https://gitlab.com/tdameritrade-tools/tdameritrade-client/commits/master) [![PyPI Version](https://badge.fury.io/py/tdameritrade-client.svg)](https://badge.fury.io/py/tdameritrade-client) [![PyPI download month](https://img.shields.io/pypi/dm/tdameritrade-client.svg)](https://pypi.python.org/pypi/tdameritrade-client/)\n\n\n# TDAmeritrade Client\n\nA tool that links to the TDA API to perform requests.\n\nRead the [docs](https://tdameritrade-client.readthedocs.io/en/latest/?#).\n\n## Installation:\nRun `pip install tdameritrade-client` within a virtual environment\n\n## Basic Usage:\nTo get started, use the following code snippet:\n\n``` python\nfrom tdameritrade_client.client import TDClient\n\ntd_client = TDClient(acct_number=<your account number>,\n                     oauth_user_id=<the id registered to the TD app you would like to authenticate with>,\n                     redirect_uri=<the redirect URI registered to the TD app>,\n                     token_path=<optional path to an existing access token>)\ntd_client.run_auth()\nacct_info = td_client.get_positions()\n```\n\n## Tests\nThis package uses poetry, which can be installed by running:\n```\ncurl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python\n```\nTo run the tests, first install the package by cloning the repo and running `poetry install` from the root of the\nrepository. Then, run `poetry run pytest tests/` from the root directory of this repository.\n',
    'author': 'Joe Castagneri',
    'author_email': 'jcastagneri@gmail.com',
    'url': 'https://gitlab.com/tdameritrade-tools/tdameritrade-client',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
