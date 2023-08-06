# -*- coding: utf-8 -*-
from distutils.core import setup

modules = \
['maker_chief']
install_requires = \
['appdirs>=1.4,<2.0',
 'click>=7.0,<8.0',
 'eth-abi>=1.3,<2.0',
 'eth-utils>=1.4,<2.0',
 'requests>=2.21,<3.0',
 'web3>=4.9,<5.0']

entry_points = \
{'console_scripts': ['maker-chief = maker_chief:main']}

setup_kwargs = {
    'name': 'maker-chief',
    'version': '0.1.2',
    'description': 'tally makerdao governance votes',
    'long_description': '# maker-chief\ntally makerdao governance votes\n\n## about\n\nthis tool fetches all `etch` and `vote` events from makerdao governance contract (see [ds-chief](https://github.com/dapphub/ds-chief)), tallies the votes and breaks them down by proposal and voters.\n\nit also tries to recover what proposals are doing assuming they are [ds-spell](https://github.com/dapphub/ds-spell) executed on [mom](https://github.com/makerdao/sai/blob/master/src/mom.sol) contract. functions like `setFee` can be additionally parsed to show more meaningful values.\n\nthe text output format is:\n\n```\n<n>. <proposal> <votes>\nspell: <func> <desc> <args>\n  <voter> <votes>\n```\n\nthe currently active proposal (`hat`) is shown in green.\n\nthe json format is self-explanatory. note that the numbers are encoded as text to avoid rounding errors.\n\n## installation\n\ninstall python 3.7 and a local ethereum node.\n\n```bash\npip3 install maker-chief \n```\n\n## usage\n\nrun `maker-chief` or `maker-chief --json`\n',
    'author': 'banteg',
    'author_email': 'banteeg@gmail.com',
    'url': 'https://github.com/banteg/maker-chief',
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
