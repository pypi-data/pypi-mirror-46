# rs3clans.py
[![PyPI](https://img.shields.io/pypi/v/rs3clans.svg)](https://pypi.org/project/rs3clans/) [![PyPI - Python Version](https://img.shields.io/pypi/pyversions/rs3clans.svg)](https://pypi.org/project/rs3clans/) [![Build Status](https://travis-ci.org/johnvictorfs/rs3clans.py.svg?branch=master)](https://travis-ci.org/johnvictorfs/rs3clans.py)

A Python 3 module wrapper for RuneScape 3 API

- [Change Log](CHANGELOG.md)

***
## Requirements:

- [`Python 3.6+`](https://www.python.org/)

- [`requests>=2.21.0`](http://docs.python-requests.org/en/master/)

***

## Setup with pip:

```bash
$ python3 -m pip install rs3clans
```

***

## Usage:

<details>
<summary>
> Players
</summary>

- Creating a Player object
    - Always check if a player actually exists before doing anything with it
```python
>>> from rs3clans import players
>>> player = players.Player(name='nriver')
>>> if player.exists:
...     pass
```

- Whether the player exists or not
```python
>>> player.exists
True
```

- Whether his Runemetrics Profile is Private or not
```python
>>> player.private_profile
False
```

- You can also pass the argument runemetrics as `False` if you don't want their runemetrics info to be set
    - This will make you unable to use some attributes from the Player class
```python
>>> player = players.Player(name='nriver', runemetrics=False)
```

- Getting a player's name
    - (if his Runemetrics Profile is private it will return the same name passed when creating object)
```python
>>> player.name
'NRiver'
```

- Getting a player's total Exp (requires Public Runemetrics Profile)
```python
>>> player.exp
1037291112
```

- Getting a player's Total Level (requires Public Runemetrics Profile)
```python
>>> player.total_level
```

- Getting a player's Combat Level (requires Public Runemetrics Profile)
```python
>>> player.combat_level
138
```

- Quests information about a player (requires Public Runemetrics Profile)
```python
>>> player.quests_not_started
32
>>> player.quests_started
5
>>> player.quests_complete
198
```

- Getting information on a specific skill of the player (requires Public Runemetrics Profile)
```python
>>> player.skill('agility').level
99
```

- Skill name is case-insensitive
```python
>>> player.skill('AtTaCk').rank
68311
```

- Can pass skill names as well as id
    - (8 = Woodcutting for example)
```python
>>> player.skill(8).exp
14054178.6
```

- Getting a player's title
```python
>>> player.title
'The Liberator'
```

- Verifying if a player's title is a suffix or not
```python
>>> player.suffix
True
```

- Getting a player's clan
```python
>>> player.clan
'Atlantis'
```
</details>

<details>
<summary>
> Clans
</summary>

- Creating a Clan object
    - Always check if a clan actually exists before doing anything with it
```python
>>> from rs3clans import clans
>>> try:
...     clan = clans.Clan('Atlantis')
... except clans.ClanNotFoundError:
...     print('Clan not found.')
```

- Getting a clan's total Exp
```python
>>> clan.exp
151349638333
```

- Getting information about a specific member in that clan
    - Clan.member attribute (dict) (requires case-sensitive name)
    - Clan.get_member() (method) (does not require case-sensitive name)
    - Returns a ClanMember Object
```python
>>> # Case-sensitive
>>> clan.member['NRiver']
ClanMember(NRiver, Overseer, 1043065027)
>>> clan.member['NRiver'].rank
'Overseer'
```

```python
>>> # Case-insensitive
>>> clan.get_member('nriver')
ClanMember(NRiver, Overseer, 1043065027)
>>> clan.get_member('nRiVeR').rank
'Overseer'
```

- Getting the number of players in a clan
```python
>>> clan.count
499
```

- Getting the average Clan Exp per player in clan
```python
>>> clan.avg_exp
303305888.44288576
```

- Iterate through a Clan
```python
>>> for member in clan:
>>>     print(f"{member} - {member.name}")
ClanMember(Pedim, Owner, 1249520826) - Pedim
ClanMember(Acriano, Overseer, 1903276564) - Acriano
ClanMember(Cogu, Overseer, 1829449412) - Cogu
ClanMember(Black bullet, Overseer, 1100767386) - Black Bullet
ClanMember(NRiver, Overseer, 1090093362) - NRiver
ClanMember(Kurenaii, Overseer, 395850997) - Kurenaii
...
```

</details>

***

## Contributing:

- Guidelines:
    - Follow Pep8 with the exception of `E501 (line too long)`

- [Fork](https://github.com/johnvictorfs/rs3clans.py/fork) the repository

- Install Dev dependencies
    - With poetry
        ```bash
        $ python3 -m virtualenv .venv
        $ poetry shell
        $ poetry install
        ```
    - Without pipenv
        ```bash
        $ python3 -m virtualenv .venv
        $ source .venv/bin/activate
        $ pip install -r requirements-dev.txt
        ```

- Run the tests to make sure everything is ok
    ```bash
    $ pytest
    ```

- Make your changes to the code in the directory `rs3clans.py/rs3clans/`

- Add necessary tests to the `rs3clans.py/tests/` directory ([`pytest docs`](https://docs.pytest.org/en/latest/))

- Run the tests again
    ```bash
    $ pytest
    ```

- Also run `flake8` just to check if the code style is also fine
    ```bash
    $ flake8 --ignore=E501 rs3clans/
    ```

- If everything went fine then send a [Pull Request](https://github.com/johnvictorfs/rs3clans.py/pulls)

***