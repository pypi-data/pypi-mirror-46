# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['mig3_client', 'mig3_client.vendors']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.0,<8.0',
 'gitpython>=2.1,<3.0',
 'pathlib2>=2.3,<3.0',
 'pytest-json>=0.4.0,<0.5.0',
 'pytest<5',
 'requests>=2.21,<3.0',
 'tomlkit>=0.5.3,<0.6.0']

entry_points = \
{'console_scripts': ['mig3 = mig3_client:mig3']}

setup_kwargs = {
    'name': 'mig3-client',
    'version': '0.5.9',
    'description': 'Send test result to Mig3 service',
    'long_description': '# ![mig3-client](https://repository-images.githubusercontent.com/183148001/d7c73680-6eaf-11e9-88b4-269c8d788541)\n## *mig3-client*: Submit your results to a mig3 service.\n\n[![Codacy Quality Badge](https://api.codacy.com/project/badge/Grade/8fbaac0868ee4261915b7c48ba8ee881)](https://app.codacy.com/app/mverteuil/mig3?utm_source=github.com&utm_medium=referral&utm_content=mverteuil/mig3-client&utm_campaign=Badge_Grade_Dashboard)\n[![Codacy Coverage Badge](https://api.codacy.com/project/badge/Coverage/fcd5f70f0c294c948c70910456661093)](https://www.codacy.com/app/mverteuil/mig3-client?utm_source=github.com&utm_medium=referral&utm_content=mverteuil/mig3-client&utm_campaign=Badge_Coverage)\n[![Build Status](https://travis-ci.com/mverteuil/mig3-client.svg?branch=master)](https://travis-ci.com/mverteuil/mig3-client)\n![Supported Python Versions](https://img.shields.io/pypi/pyversions/mig3-client.svg)\n[![Project License](https://img.shields.io/pypi/l/mig3-client.svg?color=blue)](https://github.com/mverteuil/mig3-client/blob/master/LICENSE)\n[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2Fmverteuil%2Fmig3-client.svg?type=shield)](https://app.fossa.com/projects/git%2Bgithub.com%2Fmverteuil%2Fmig3-client?ref=badge_shield)\n![Project Status](https://img.shields.io/pypi/status/mig3-client.svg)\n[![PyPI version](https://img.shields.io/pypi/v/mig3-client.svg)](https://badge.fury.io/py/mig3-client)\n[![PyPI downloads](https://img.shields.io/pypi/dm/mig3-client.svg?color=darklime)](https://pypi.org/project/mig3-client/)\n[![Manpower](https://img.shields.io/github/contributors/mverteuil/mig3-client.svg?color=red&label=manpower)](https://github.com/mverteuil/mig3-client/graphs/contributors)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/python/black)\n[![FOSSA Status](https://app.fossa.io/api/projects/git%2Bgithub.com%2Fmverteuil%2Fmig3-client.svg?type=shield)](https://app.fossa.io/projects/git%2Bgithub.com%2Fmverteuil%2Fmig3-client?ref=badge_shield)\n\n## See Also\n\n-   [mig3](https://github.com/mverteuil/mig3): Detect regressions in your python3 migration!\n\n## Basic setup\n\nInstall it:\n```\n$ pip install mig3-client\n```\n\nRun the application:\n```\n$ mig3 --help\n```\n\n## Developer setup\n\nInstall dependencies:\n```\n$ poetry install\n```\n\nTo run the tests for the current environment:\n```\n$ poetry shell\n$ py.test\n```\n\nTo run the tests for all environments:\n```\n$ tox\n```\n\n## License\n\n[![FOSSA Status](https://app.fossa.io/api/projects/git%2Bgithub.com%2Fmverteuil%2Fmig3-client.svg?type=large)](https://app.fossa.io/projects/git%2Bgithub.com%2Fmverteuil%2Fmig3-client?ref=badge_large)\n',
    'author': 'Matthew de Verteuil',
    'author_email': 'onceuponajooks@gmail.com',
    'url': 'https://github.com/mverteuil/mig3-client',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, !=3.5.*',
}


setup(**setup_kwargs)
