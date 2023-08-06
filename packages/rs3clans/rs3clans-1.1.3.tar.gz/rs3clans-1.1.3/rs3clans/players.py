from dataclasses import dataclass
import json

import requests


@dataclass
class Player:
    """Class with attributes of a Runescape Player using Jagex's RS3 API

    Most of Runescape 3's API can be accessed at: http://runescape.wikia.com/wiki/Application_programming_interface

    ...

    Args:
        name (str): Name of the Player, gets set to case-sensitive name later if his RuneMetrics profile is not private.
        If you're also working with clans and the player's profile is private, name should be passed case-sensitively.
        Otherwise some clan attributes will not be available.

        runemetrics (bool): Whether or not Runemetrics player info should be set or not, slows down creating the object,
        but provides more attributes and methods.

    Attributes:
        name (str): Name of the Player, gets set to case-sensitive name later if his RuneMetrics profile is not private.

        metrics_info (str): Runemetrics Info in dictionary format about the player.

        exp (int or None): Total Exp of the player, or None if private_profile is True.

        combat_level (int or None): Total Combat Level of the player, or None if private_profile is True.

        total_level (int or None): Total Skill Level of the player, or None if private_profile is True.

        quests_not_started (int): Number of quests the player has not started.

        quests_started (int): Number of the quests the player has started.

        quests_complete (int): Number of quests the player has completed.

        private_profile (bool): Whether the player has a private RuneMetrics profile or not.

        exists (bool): Whether the player exists or not.

        details_status_code (int): The status code of the GET request to RS3 Player Details API

        runemetrics_status_code (int): The status code of the GET request to RS3 Player Runemetrics API

    Raises:
        ConnectionError
            If connecting to any of RS3's API related to players fails.
    """
    name: str
    runemetrics: bool = True

    metrics_info: dict = None
    exp: int = None
    combat_level: int = None
    total_level: int = None
    quests_not_started: int = None
    quests_started: int = None
    quests_complete: int = None
    skill_values: list = None
    details_status_code: int = None
    runemetrics_status_code: int = None
    private_profile: bool = True
    exists: bool = True

    def __post_init__(self) -> None:
        if not self.name:
            raise TypeError("Player name cannot be null.")

        self.info = self._dict_info()
        self.suffix = self.info['is_suffix']
        self.title = self.info['title']

        # TODO: The check below is a band-aid fix that marks self.exists as False even if 'runemetrics' parameter
        # is passed as False when creating Player object, a real way to check if a player exists needs to be added
        if not self._valid_username(self.name):
            self.exists = False

        if self.runemetrics:
            self.set_runemetrics_info()

        try:
            self.clan = self.info['clan']
        except KeyError:
            self.clan = None

    @staticmethod
    def _valid_username(username: str) -> bool:
        """
        Checks if a username is in the valid character limit set by Jagex
        and if it doesn't have any invalid characters in it.

        Args:
            username (str): The username to be checked if valid or not

        Returns:
            bool. True if the username is valid, False if it is not
        """
        if len(username) > 12:
            return False
        banned_chars = (
            '!', '@', '#', '$', '%', '¨', '&', '*', '(', ')', '[', ']', ',', '.', '~', '^',
            '{', '}', ':', ';', "'",
            '"', 'ç', 'Ç', '?', '/', '°', '|', '\\', '`', '=', '+', '¬',
            '¹', '²', '³', '£', '¢', 'ª', 'º'
        )
        if any(char in username for char in banned_chars):
            return False
        return True

    def _raw_info(self) -> str:
        """
        Gets JsonP information on a player, in string format.

        Returns:
            str. JsonP information on player, converted to string.

        Raises:
            ConnectionError
                If connecting to the RS3 Runemetrics profile API was not possible.

        ------
        .. note::
            Has to be formatted correctly into Json or other formats to be worked with properly first.
        """

        info_url = (f"http://services.runescape.com/m=website-data/"
                    f"playerDetails.ws?names=%5B%22{self.name}%22%5D&callback=jQuery000000000000000_0000000000&_=0")
        response = requests.get(info_url)
        self.details_status_code = response.status_code
        if response.status_code != 200:
            raise ConnectionError(f'Not able to connect to RS3 playerDetails API. Status code: {response.status_code}')
        return str(response.content)

    def _dict_info(self) -> dict:
        """
        Gets the raw string info from self._raw_info() and formats it into Dictionary format.:
        Used to set self.info.

        Returns:
            dict. Dictionary is formatted as follows::
                >>> player_info = {
                ... 'is_suffix': True,
                ... 'recruiting': True,
                ... 'name': 'nriver',
                ... 'clan': 'Atlantis',
                ... 'title': 'the Liberator'
                ... }
            is_suffix (bool): If the player's title is a Suffix or not

            recruiting (bool): If the player's clan is set as Recruiting or not

            name (str): The player's name, passed as is when creating object Player

            clan (str): The player's clan name

            title (str): The player's current title
        """
        str_info = self._raw_info()
        info_list = []

        # str_info[36] = Start of json format in URL '{'
        for letter in str_info[36:]:
            info_list.append(letter)
            if letter == '}':
                break
        info_list = ''.join(info_list)
        info_dict = json.loads(info_list)
        info_dict['is_suffix'] = info_dict['isSuffix']
        del info_dict['isSuffix']
        return info_dict

    def set_runemetrics_info(self) -> None:
        """
        Sets Runemetrics info attributes for the Player.

        Attributes set:
            name (str): Case-sensitive player username.

            exp (int): Total Exp of the Player.

            combat_level (int): Total Combat Level of the Player.

            total_level (int): Total Skill Level of the Player.
        """
        # If user's runemetrics profile is private, self.name will be the same as passed when creating object.
        # Otherwise it will get the correct case-sensitive name from his runemetrics profile.
        # Some other info like Total exp, Combat level and Total level will be created as well.
        self.metrics_info = self.runemetrics_info()
        if self.metrics_info:
            if self.metrics_info.get('name'):
                self.name = self.metrics_info.get('name')
            self.exp = self.metrics_info.get('totalxp')
            self.combat_level = self.metrics_info.get('combatlevel')
            self.total_level = self.metrics_info.get('totalskill')
            self.quests_not_started = self.metrics_info.get('questsnotstarted')
            self.quests_started = self.metrics_info.get('questsstarted')
            self.quests_complete = self.metrics_info.get('questscomplete')
            self.skill_values = self.metrics_info.get('skillvalues')

    def runemetrics_info(self):
        """
        Gets player info from Runemetrics' API.
        Sets `private_profile` to True if his Runemetrics profile is found to be Private.

        Format::
            >>> {
            ... "magic":16216354,
            ... "questsstarted":5,
            ... "totalskill":2715,
            ... "questscomplete":198,
            ... "questsnotstarted":32,
            ... "totalxp":1037291112,
            ... "ranged":84195157,
            ... "activities":[
            ...
            ... ],
            ... # "skillvalues" has all skills and they are marked with their respective ID's, only 3 were shown here
            ... "skillvalues":[
            ...    {
            ...       "level":120,
            ...       "xp":1857550415,
            ...       "rank":12014,
            ...       "id":26
            ...    },
            ...    {
            ...       "level":99,
            ...       "xp":1202360390,
            ...       "rank":10370,
            ...       "id":6
            ...    },
            ...    {
            ...       "level":99,
            ...       "xp":841951573,
            ...       "rank":26941,
            ...       "id":3
            ...    },
            ... ],
            ... "name":"NRiver",
            ... "rank":"36,708",
            ... "melee":527931306,
            ... "combatlevel":138,
            ... "loggedIn":"false"
            ... }

        Returns:
            dict or bool. Runemetrics player info if the player profile is public, or False if it is Private.

        Raises:
            ConnectionError
                If connecting to the RS3 Runemetrics profile API was not possible.
        """
        user_name = self.name.replace(' ', '%20')
        info_url = f"https://apps.runescape.com/runemetrics/profile/profile?user={user_name}&activities=0"
        response = requests.get(info_url)
        self.runemetrics_status_code = response.status_code
        if response.status_code != 200:
            raise ConnectionError(
                f'Not able to connect to RS3 Runemetrics player profile API. Status code: {response.status_code}')
        json_info = response.json()
        if json_info.get('error') == 'PROFILE_PRIVATE':
            self.private_profile = True
            return None
        elif json_info.get('error') == 'NO_PROFILE':
            self.private_profile = False
            self.exists = False
            return None
        else:
            self.private_profile = False
            return json_info

    def skill(self, skill: str or int):
        """
        Gets information on a specific skill from the Player

        Usage::
            >>> # Example of usage of the method skill()
            >>> player = Player('NRiver')
            >>> player.skill('agility').level
            99
            >>> # Can pass skill names as well as id
            >>> # (8 = Woodcutting for example)
            >>> player.skill(8).exp
            14054178.6
            >>> player.skill('AtTaCk').rank
            68311

        Args:
            skill (str or int): Skill name or id to get info of

        Returns:
            Skill.
            Attributes of Skill
            --------------------
                exp (int): Total exp the Player has in that skill

                xp (int): Total exp the Player has in that skill

                level (int): The level the Player has in that skill

                rank (int): The Rank the Player has in that skill
        """
        skills_index = {
            0: 'attack',
            1: 'defence',
            2: 'strength',
            3: 'constitution',
            4: 'ranged',
            5: 'prayer',
            6: 'magic',
            7: 'cooking',
            8: 'woodcutting',
            9: 'fletching',
            10: 'fishing',
            11: 'firemaking',
            12: 'crafting',
            13: 'smithing',
            14: 'mining',
            15: 'herblore',
            16: 'agility',
            17: 'thieving',
            18: 'slayer',
            19: 'farming',
            20: 'runecrafting',
            21: 'hunter',
            22: 'construction',
            23: 'summoning',
            24: 'dungeoneering',
            25: 'divination',
            26: 'invention',
        }

        try:
            skill = int(skill)
            for _skill in self.skill_values:
                if _skill['id'] == skill:
                    return Skill(name=skills_index[skill], skill=_skill)
        except ValueError:
            skill = skill.lower()
            for index, value in skills_index.items():
                if skill == value:
                    skill = index
                    for _skill in self.skill_values:
                        if _skill['id'] == skill:
                            return Skill(name=skills_index[skill], skill=_skill)

    def __repr__(self):
        return f"Player(name={repr(self.name)}, clan={repr(self.clan)}, exists={self.exists})"


@dataclass
class Skill:
    """
    Represents a RuneScape 3 Skill

    Args:
        name (str): Name of the Skill

        skill (dict): Skill in dictionary format as it is in RuneScape's 3 API

    Attributes:
        exp (int): Total Exp the player has in the skill

        xp (int): Total Exp the player has in the skill

        level (int): Total Level the player has in the skill

        rank (int): Rank the player has in the skill

        id (int): The ID of the Skill
    """
    name: str
    skill: dict

    exp: int = None
    xp: int = None
    level: int = None
    rank: int = None
    id: int = None

    def __post_init__(self):
        self.exp = self.skill.get('xp') / 10
        self.xp = self.exp

        self.level = self.skill.get('level')
        self.rank = self.skill.get('rank')
        self.id = self.skill.get('id')

    def __str__(self):
        return self.name
