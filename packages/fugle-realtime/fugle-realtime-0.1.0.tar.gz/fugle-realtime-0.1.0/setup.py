# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['fugle_realtime', 'fugle_realtime.intraday']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=0.24.2,<0.25.0', 'requests>=2.22,<3.0']

setup_kwargs = {
    'name': 'fugle-realtime',
    'version': '0.1.0',
    'description': 'Fugle Realtime',
    'long_description': '# fugle-realtime-py\n\n## Contributing\n\nInstall [`poetry`](https://poetry.eustace.io/) if not yet installed:\n\n```sh\ncurl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python\n```\n\nThen install dependencies and setup [`pre-commit`](https://pre-commit.com/):\n\n```sh\npoetry install\n\npoetry run pre-commit install\n```\n\nCode formatting using [`black`](https://black.readthedocs.io/en/stable/):\n\n```sh\npoetry run black .\n```\n\nTesting using [`pytest`](https://pytest.org):\n\n```sh\npoetry run pytest\n```\n',
    'author': 'Fortuna Intelligence Co., Ltd.',
    'author_email': 'development@fugle.tw',
    'url': 'https://developer.fugle.tw/realtime',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
