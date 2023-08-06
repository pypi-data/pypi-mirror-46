# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['celery_singleton', 'celery_singleton.backends']

package_data = \
{'': ['*']}

install_requires = \
['celery>=4,<5', 'redis>=2']

setup_kwargs = {
    'name': 'celery-singleton',
    'version': '0.2.0',
    'description': 'Prevent duplicate celery tasks',
    'long_description': None,
    'author': 'Steinthor Palsson',
    'author_email': 'steini90@gmail.com',
    'url': 'https://github.com/steinitzu/spoffy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
