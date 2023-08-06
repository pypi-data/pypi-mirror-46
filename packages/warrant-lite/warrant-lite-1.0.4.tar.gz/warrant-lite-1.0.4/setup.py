# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['warrant_lite']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.9,<2.0',
 'envs>=1.3,<2.0',
 'python-jose>=3.0,<4.0',
 'requests>=2.22,<3.0']

setup_kwargs = {
    'name': 'warrant-lite',
    'version': '1.0.4',
    'description': 'Small Python library for process SRP requests for AWS Cognito. This library was initially included in the [Warrant](https://www.github.com/capless/warrant) library. We decided to separate it because not all projects and workfows need all of the helper classes and functions in Warrant.',
    'long_description': None,
    'author': 'Brian Jinwright',
    'author_email': 'brian@ipoots.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
