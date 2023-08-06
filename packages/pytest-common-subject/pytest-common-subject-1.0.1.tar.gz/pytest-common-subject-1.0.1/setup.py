# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['pytest_common_subject']

package_data = \
{'': ['*']}

install_requires = \
['lazy-object-proxy>=1.3.1,<2.0.0',
 'pytest-fixture-order==0.1.1',
 'pytest-lambda>=0.1.0',
 'pytest>=3.6,<4.6']

setup_kwargs = {
    'name': 'pytest-common-subject',
    'version': '1.0.1',
    'description': 'pytest framework for testing different aspects of a common method',
    'long_description': '# pytest-common-subject\n[![pytest-common-subject PyPI version](https://badge.fury.io/py/pytest-common-subject.svg)](https://pypi.python.org/pypi/pytest-common-subject/)\n[![pytest-common-subject PyPI pyversions](https://img.shields.io/pypi/pyversions/pytest-common-subject.svg)](https://pypi.python.org/pypi/pytest-common-subject/)\n[![pytest-common-subject PyPI license](https://img.shields.io/pypi/l/pytest-common-subject.svg)](https://pypi.python.org/pypi/pytest-common-subject/)\n\n**pytest-common-subject** is a "framework" for organizing tests to reduce boilerplate while writing, improve skimmability when reading, and bolster parallelization when executing the suite.\n\nTo utilize this framework, we first choose a single function that our group of tests will all call — in other words, an entry point, or a _common subject_. This function will be automatically called before each of our tests, with args and kwargs that can be customized by overriding fixtures — enabling child test classes to make HTTP requests as a different user, or to use a different cache backend, or to change the value of a monkeypatched method.\n\nThe return value of the chosen function will be passed as a fixture to each test. To reap the full benefits of the framework, create separate tests to verify different aspects of the return value. Was the response status code a 200? Did the response contain the expected data? Were the expected rows created in the database? By using separate tests for each of these aspects, we can pinpoint and correct multiple bugs at once, instead of getting sucked into a fix-test-fix cycle with its chorus of "oh, bother, not again!"\n',
    'author': 'Zach "theY4Kman" Kanzler',
    'author_email': 'z@perchsecurity.com',
    'url': 'https://github.com/usePF/pytest-common-subject',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
