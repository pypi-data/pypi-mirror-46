# -*- coding: utf-8 -*-
from distutils.core import setup

modules = \
['swpy']
setup_kwargs = {
    'name': 'swpy',
    'version': '0.1.1',
    'description': 'A simple, yet useful stopwatch library.',
    'long_description': "# swpy: A simple, yet useful stopwatch library for python\n\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/swpy.svg?style=flat-square)](https://pypi.org/project/swpy/)\n[![PyPI](https://img.shields.io/pypi/v/swpy.svg?style=flat-square)](https://pypi.org/project/swpy/)\n[![CircleCI](https://img.shields.io/circleci/project/github/peinan/swpy.svg?logo=circleci&style=flat-square)](https://circleci.com/gh/peinan/swpy/tree/master)\n[![codecov](https://img.shields.io/codecov/c/gh/peinan/swpy.svg?logo=codecov&style=flat-square)](https://codecov.io/gh/peinan/swpy)\n[![PyPI - License](https://img.shields.io/pypi/l/swpy.svg?color=blue&style=flat-square)](https://github.com/peinan/swpy/blob/master/LICENSE)\n\n## Requirements\n\n- Python 3.6+\n\n## Install\n\n```bash\n$ pip install swpy\n```\n\n## Usage\n\n```python\n>>> from swpy import Timer\n>>> import time\n\n\n# the simplest use\n>>> with Timer():\n...   time.sleep(1)\n\n[timer-1557406243.3309178] started.\n[timer-1557406243.3309178] finish time: 1.00 sec.\n\n\n# name the timer for visibility\n>>> with Timer(name='test timer'):\n...     time.sleep(1)\n\n[test timer] started.\n[test timer] finish time: 1.00 sec.\n\n\n# use your own logger\n>>> from logzero import logger\n>>> import logging\n>>> with Timer(name='test timer', logger=logger, level=logging.DEBUG):\n...     time.sleep(1)\n\n[D 190510 14:41:59 swpy:15] [test timer] started.\n[D 190510 14:42:00 swpy:15] [test timer] finish time: 1.01 sec.\n\n\n# process the timer result with your own function with callback\n## define a slack notification function\n>>> import requests, json\n>>> def send_slack(msg):\n...     requests.post(SLACK_URL, json.dumps({'text': msg}))\n\n## just specify the callback argument\n>>> with Timer(name='experiment-1', logger=logger, level=logging.DEBUG, callback=send_slack):\n...     time.sleep(1)\n[D 190510 14:48:17 swpy:15] [experiment-1] started.\n[D 190510 14:48:18 swpy:15] [experiment-1] finish time: 1.01 sec.\n```\n\n## License\n\nMIT\n",
    'author': 'Peinan ZHANG',
    'author_email': 'peinan7@gmail.co.jp',
    'url': 'https://github.com/peinan/swpy',
    'py_modules': modules,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
