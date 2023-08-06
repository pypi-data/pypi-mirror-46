# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['rs3clans']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.21,<3.0']

extras_require = \
{':python_version >= "3.6" and python_version < "3.7"': ['dataclasses>=0.6,<0.7']}

setup_kwargs = {
    'name': 'rs3clans',
    'version': '1.1.3',
    'description': "A Python 3 module wrapper for RuneScape 3's API",
    'long_description': '# rs3clans.py\n[![PyPI](https://img.shields.io/pypi/v/rs3clans.svg)](https://pypi.org/project/rs3clans/) [![PyPI - Python Version](https://img.shields.io/pypi/pyversions/rs3clans.svg)](https://pypi.org/project/rs3clans/) [![Build Status](https://travis-ci.org/johnvictorfs/rs3clans.py.svg?branch=master)](https://travis-ci.org/johnvictorfs/rs3clans.py)\n\nA Python 3 module wrapper for RuneScape 3 API\n\n- [Change Log](CHANGELOG.md)\n\n***\n## Requirements:\n\n- [`Python 3.6+`](https://www.python.org/)\n\n- [`requests>=2.21.0`](http://docs.python-requests.org/en/master/)\n\n***\n\n## Setup with pip:\n\n```bash\n$ python3 -m pip install rs3clans\n```\n\n***\n\n## Usage:\n\n<details>\n<summary>\n> Players\n</summary>\n\n- Creating a Player object\n    - Always check if a player actually exists before doing anything with it\n```python\n>>> from rs3clans import players\n>>> player = players.Player(name=\'nriver\')\n>>> if player.exists:\n...     pass\n```\n\n- Whether the player exists or not\n```python\n>>> player.exists\nTrue\n```\n\n- Whether his Runemetrics Profile is Private or not\n```python\n>>> player.private_profile\nFalse\n```\n\n- You can also pass the argument runemetrics as `False` if you don\'t want their runemetrics info to be set\n    - This will make you unable to use some attributes from the Player class\n```python\n>>> player = players.Player(name=\'nriver\', runemetrics=False)\n```\n\n- Getting a player\'s name\n    - (if his Runemetrics Profile is private it will return the same name passed when creating object)\n```python\n>>> player.name\n\'NRiver\'\n```\n\n- Getting a player\'s total Exp (requires Public Runemetrics Profile)\n```python\n>>> player.exp\n1037291112\n```\n\n- Getting a player\'s Total Level (requires Public Runemetrics Profile)\n```python\n>>> player.total_level\n```\n\n- Getting a player\'s Combat Level (requires Public Runemetrics Profile)\n```python\n>>> player.combat_level\n138\n```\n\n- Quests information about a player (requires Public Runemetrics Profile)\n```python\n>>> player.quests_not_started\n32\n>>> player.quests_started\n5\n>>> player.quests_complete\n198\n```\n\n- Getting information on a specific skill of the player (requires Public Runemetrics Profile)\n```python\n>>> player.skill(\'agility\').level\n99\n```\n\n- Skill name is case-insensitive\n```python\n>>> player.skill(\'AtTaCk\').rank\n68311\n```\n\n- Can pass skill names as well as id\n    - (8 = Woodcutting for example)\n```python\n>>> player.skill(8).exp\n14054178.6\n```\n\n- Getting a player\'s title\n```python\n>>> player.title\n\'The Liberator\'\n```\n\n- Verifying if a player\'s title is a suffix or not\n```python\n>>> player.suffix\nTrue\n```\n\n- Getting a player\'s clan\n```python\n>>> player.clan\n\'Atlantis\'\n```\n</details>\n\n<details>\n<summary>\n> Clans\n</summary>\n\n- Creating a Clan object\n    - Always check if a clan actually exists before doing anything with it\n```python\n>>> from rs3clans import clans\n>>> try:\n...     clan = clans.Clan(\'Atlantis\')\n... except clans.ClanNotFoundError:\n...     print(\'Clan not found.\')\n```\n\n- Getting a clan\'s total Exp\n```python\n>>> clan.exp\n151349638333\n```\n\n- Getting information about a specific member in that clan\n    - Clan.member attribute (dict) (requires case-sensitive name)\n    - Clan.get_member() (method) (does not require case-sensitive name)\n    - Returns a ClanMember Object\n```python\n>>> # Case-sensitive\n>>> clan.member[\'NRiver\']\nClanMember(NRiver, Overseer, 1043065027)\n>>> clan.member[\'NRiver\'].rank\n\'Overseer\'\n```\n\n```python\n>>> # Case-insensitive\n>>> clan.get_member(\'nriver\')\nClanMember(NRiver, Overseer, 1043065027)\n>>> clan.get_member(\'nRiVeR\').rank\n\'Overseer\'\n```\n\n- Getting the number of players in a clan\n```python\n>>> clan.count\n499\n```\n\n- Getting the average Clan Exp per player in clan\n```python\n>>> clan.avg_exp\n303305888.44288576\n```\n\n- Iterate through a Clan\n```python\n>>> for member in clan:\n>>>     print(f"{member} - {member.name}")\nClanMember(Pedim, Owner, 1249520826) - Pedim\nClanMember(Acriano, Overseer, 1903276564) - Acriano\nClanMember(Cogu, Overseer, 1829449412) - Cogu\nClanMember(Black\xa0bullet, Overseer, 1100767386) - Black Bullet\nClanMember(NRiver, Overseer, 1090093362) - NRiver\nClanMember(Kurenaii, Overseer, 395850997) - Kurenaii\n...\n```\n\n</details>\n\n***\n\n## Contributing:\n\n- Guidelines:\n    - Follow Pep8 with the exception of `E501 (line too long)`\n\n- [Fork](https://github.com/johnvictorfs/rs3clans.py/fork) the repository\n\n- Install Dev dependencies\n    - With poetry\n        ```bash\n        $ python3 -m virtualenv .venv\n        $ poetry shell\n        $ poetry install\n        ```\n    - Without pipenv\n        ```bash\n        $ python3 -m virtualenv .venv\n        $ source .venv/bin/activate\n        $ pip install -r requirements-dev.txt\n        ```\n\n- Run the tests to make sure everything is ok\n    ```bash\n    $ pytest\n    ```\n\n- Make your changes to the code in the directory `rs3clans.py/rs3clans/`\n\n- Add necessary tests to the `rs3clans.py/tests/` directory ([`pytest docs`](https://docs.pytest.org/en/latest/))\n\n- Run the tests again\n    ```bash\n    $ pytest\n    ```\n\n- Also run `flake8` just to check if the code style is also fine\n    ```bash\n    $ flake8 --ignore=E501 rs3clans/\n    ```\n\n- If everything went fine then send a [Pull Request](https://github.com/johnvictorfs/rs3clans.py/pulls)\n\n***',
    'author': 'johnvictorfs',
    'author_email': 'johnvictorfs@gmail.com',
    'url': 'https://github.com/johnvictorfs/rs3clans.py',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
