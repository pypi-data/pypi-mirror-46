# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['prevenger',
 'prevenger.cache',
 'prevenger.crypto',
 'prevenger.gen',
 'prevenger.inspector',
 'prevenger.kit',
 'prevenger.orm',
 'prevenger.orm.smart_filter',
 'prevenger.records',
 'prevenger.str_kit',
 'prevenger.validator']

package_data = \
{'': ['*']}

install_requires = \
['click_completion>=0.5.1,<0.6.0',
 'click_didyoumean>=0.0.3,<0.0.4',
 'crayons>=0.2.0,<0.3.0',
 'requests',
 'sqlalchemy',
 'werkzeug']

entry_points = \
{'console_scripts': ['prevenger-cli = prevenger.cli:main']}

setup_kwargs = {
    'name': 'prevenger',
    'version': '0.0.5',
    'description': 'final commom utils for prevengers',
    'long_description': '# prevenger\n\n[![Build Status](https://travis-ci.org/twocucao/prevenger.svg?branch=master)](https://travis-ci.org/twocucao/prevenger)\n![pyversions](https://img.shields.io/badge/python%20-3.7%2B-blue.svg)\n![pypi](https://img.shields.io/pypi/v/nine.svg)\n[![contributions welcome](https://img.shields.io/badge/contributions-welcome-ff69b4.svg)](https://github.com/twocucao/prevenger/issues)\n\n平时经常使用的代码，拷贝在身边，一用好多年\n\n> 紧跟社区最佳实践\n\n## 感谢\n\n> 感谢开源社区人的无私奉献\n\n---\nChangeLog:\n - 2019-05-09: 初始化\n\n## License\n\nMIT\n\n',
    'author': 'twocucao',
    'author_email': 'twocucao@gmail.com',
    'url': 'https://github.com/twocucao/prevengers',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
