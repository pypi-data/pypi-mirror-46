# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['fugle_realtime']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=0.24.2,<0.25.0', 'requests>=2.22,<3.0']

setup_kwargs = {
    'name': 'fugle-realtime',
    'version': '0.1.7',
    'description': 'Fugle Realtime',
    'long_description': '# fugle-realtime-py\n\n## Documentation\n\nhttps://developer.fugle.tw/realtime\n\n## Installation\n\n```sh\npip install fugle-realtime\n```\n\n## Usage\n\n```py\nfrom fugle_realtime import intraday\n```\n\n### [`intraday.chart`](https://developer.fugle.tw/realtime/document#/Intraday/get_intraday_chart): https://api.fugle.tw/realtime/v0/intraday/chart\n\n```py\nintraday.chart(apiToken="demo", output="dataframe", symbolId="2884")\n```\n\n### [`intraday.meta`](https://developer.fugle.tw/realtime/document#/Intraday/get_intraday_meta): https://api.fugle.tw/realtime/v0/intraday/meta\n\n```py\nintraday.meta(apiToken="demo", output="dataframe", symbolId="2884")\n```\n\n### [`intraday.quote`](https://developer.fugle.tw/realtime/document#/Intraday/get_intraday_quote): https://api.fugle.tw/realtime/v0/intraday/quote\n\n```py\nintraday.quote(apiToken="demo", output="dataframe", symbolId="2884")\n```\n\n### [`intraday.trades`](https://developer.fugle.tw/realtime/document#/Intraday/get_intraday_trades): https://api.fugle.tw/realtime/v0/intraday/trades\n\n```py\nintraday.trades(apiToken="demo", output="dataframe", symbolId="2884")\n```\n\n`output="dataframe"` will return [pandas](https://pandas.pydata.org/) [`DataFrame`](https://pandas.pydata.org/pandas-docs/stable/reference/frame.html), which is the default. `output="raw"` will return [python](https://www.python.org/) built-in [`dict`](https://docs.python.org/3/library/stdtypes.html#dict) or [`list`](https://docs.python.org/3/library/stdtypes.html#list) accordingly.\n\n`symbolId="2884"` is only allowed when `apiToken="demo"`. To access more `symbolId`, you will have to get your own `apiToken`. Please visit https://developer.fugle.tw/realtime/apiToken for detailed instructions.\n\nFor complete documentation of each URL specified above, please visit https://developer.fugle.tw/realtime/document.\n\n## Contributing\n\nGit clone the repository:\n\n```sh\ngit clone https://github.com/fortuna-intelligence/fugle-realtime-py.git\ncd fugle-realtime-py\n```\n\nInstall [`poetry`](https://poetry.eustace.io/) if not yet installed:\n\n```sh\ncurl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python\n```\n\nThen install dependencies and setup [`pre-commit`](https://pre-commit.com/):\n\n```sh\npoetry install\npoetry run pre-commit install\n```\n\nCode formatting using [`black`](https://black.readthedocs.io/en/stable/):\n\n```sh\npoetry run black .\n```\n\nTesting using [`pytest`](https://pytest.org):\n\n```sh\npoetry run pytest\n```\n\n## Publishing\n\n### [`PyPI`](https://pypi.org/): [`fugle-realtime`](https://pypi.org/project/fugle-realtime/)\n\n```sh\npoetry publish --build --repository pypi --username username --password password\n```\n',
    'author': 'Fortuna Intelligence Co., Ltd.',
    'author_email': 'development@fugle.tw',
    'url': 'https://developer.fugle.tw/realtime',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
