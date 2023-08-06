# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['amipwned']

package_data = \
{'': ['*']}

install_requires = \
['aiodns>=2.0,<3.0',
 'aiohttp>=3.5,<4.0',
 'aioredis>=1.2,<2.0',
 'asyncpg>=0.18.3,<0.19.0',
 'cchardet>=2.1,<3.0',
 'psycopg2>=2.8,<3.0']

entry_points = \
{'console_scripts': ['amipwned = amipwned.amipwned:main']}

setup_kwargs = {
    'name': 'amipwned',
    'version': '0.2.0',
    'description': 'A minimal self-hosted haveibeenpwned application.',
    'long_description': None,
    'author': 'Michael',
    'author_email': 'michael@dubell.io',
    'url': 'https://github.com/mjdubell/amipwned',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
