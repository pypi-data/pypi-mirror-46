from dataclasses import dataclass
import csv

import requests


class ClanNotFoundError(Exception):
    """
    Error exception to be called when a clan is not found when trying to read the clan's URL using Rs3's Official API.

    Correct error handling when reading a clan::
        >>> import rs3clans
        >>> try:
        ...     clan_name = "oasdiuahsiubasiufbasuf"
        ...     clan = rs3clans.Clan(name=clan_name)
        ... except rs3clans.ClanNotFoundError:
        ...     print("Exception encountered!")
        Exception encountered!
    """

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


@dataclass
class ClanMember:
    """
    Represents Member of a Clan

    Args:
        name (str): Name of the Clan Member
        rank (str): Rank of the Clan Member
        exp (int): Clan Exp of the Clan Member
    """
    name: str
    rank: str
    exp: int

    def __repr__(self) -> str:
        return f"ClanMember({self.name}, {self.rank}, {self.exp})"


@dataclass
class Clan:
    """Class with attributes of a Runescape Clan using Jagex's RS3 API

    Most of Runescape 3's API can be accessed at: http://runescape.wikia.com/wiki/Application_programming_interface

    ...

    Args:
        name (str): The name of the clan. Does not need to be case-sensitive.
    Kwargs:
        update_stats (bool): If True, updated stats for the Clan will be requested after creating the object and set.
        set_exp (bool): If True, the `exp` attribute will be set with the total Exp from the clan. False by default.
        set_dict (bool): If True, `member` attribute (dict) will be set with all members of the clan. True by default.

    Attributes:
        name (str): The name of the clan. Set when creating object.
        exp (int or None): The total Exp of the clan, or None if argument set_exp is False (False by default).
        member (dict or None): All info from members in the clan in dictionary format as below::
            >>> member_info = {
            ...     'player_1': {
            ...         'exp': 225231234,
            ...         'rank': 'Leader'
            ...     },
            ...     'player_2': {
            ...     'exp': 293123082,
            ...     'rank': 'Overseer'
            ...    },
            ... }
        or None if argument set_dict is False (True by default).
    count (int): The number of members in the Clan.
    avg_exp (int or None): The average clan exp per member in the Clan.

    Raises:
        ClanNotFoundError
            If an invalid clan name is passed when creating object Clan.
    """

    name: str
    update_stats: bool = True
    set_exp: bool = False
    set_dict: bool = True

    exp: int = None
    member: dict = None
    count: int = None
    avg_exp: float = None

    def __post_init__(self) -> None:
        if not self.name:
            raise TypeError("Clan name cannot be null.")
        if self.update_stats:
            self.update()

    def update(self, clan_list: list = None) -> None:
        """Updates all the Clan stats"""
        if not clan_list:
            clan_list = self.parse_clan_list(self.request_clan_list())

        if self.set_exp:
            self.exp = self._list_sum(clan_list)
        if self.set_dict:
            self.member = self.dict_lookup(clan_list)
            self.count = len(self.member)
        if self.set_exp and self.set_dict:
            self.avg_exp = self.exp / self.count

    @property
    def leader(self):
        """Finds the Clan leader in the clan member dict attribute"""
        for key, member in self.member.items():
            if member.rank == 'Owner':
                return member

    def request_clan_list(self) -> str:
        """Requests a Clan list in csv format from RS3's API from the Clan's Name"""

        clan_url = f'http://services.runescape.com/m=clan-hiscores/members_lite.ws?clanName={self.name}'

        with requests.Session() as session:
            download = session.get(clan_url)
            return download.content.decode('windows-1252')

    def parse_clan_list(self, decoded: str) -> list:
        """
        Parses a Clan List csv and returns it in a Python List

        Returns:
            list. All players information from a clan in list format like so::
                    >>> clan_list = [
                    ... ['Clanmate', ' Clan Rank', ' Total XP', ' Kills'],
                    ... ['Pedim', 'Owner', '739711654', '2'],
                    ... ['Tusoroxo', 'Deputy Owner', '1132958333', '0'],
                    ... ]
        """

        clan_list = list(csv.reader(decoded.splitlines(), delimiter=','))

        if clan_list[0][0] != "Clanmate":
            raise ClanNotFoundError(f"Couldn't find clan: {self.name}")

        for row in clan_list:
            # Replacing non-breaking spaces with actual spaces
            row[0] = ' '.join(row[0].split())
        return clan_list

    @staticmethod
    def dict_lookup(clan_list: list) -> dict:
        """

        Used for getting all information available from a clan using Rs3's Clan API.

        Contrary to `list_lookup` it returns it as a Dictionary format instead.
        The dict format makes easier to find info specific to certain members of the Clan instead of looping over it.

        Args:
            clan_list (list): The clan list to make the dictionary for

        Returns:
            dict[str, ClanMember]. Information from all members in the clan in dictionary format for ease of access.
        """
        return {row[0]: ClanMember(row[0], row[1], int(row[2])) for row in clan_list[1:]}

    def get_member(self, name: str) -> ClanMember:
        """

        Used for searching information about a clan member by passing in its name case insensitively.

        Args:
            name (str): The name of the player to be searched in clan.

        Returns:
            ClanMember. ClanMember object of the found (if found) player.
        """
        for key, value in self.member.items():
            if key.lower() == name.lower():
                return value

    @staticmethod
    def _list_sum(clan_list: list) -> int:
        """

        Returns the Exp sum of a clan list.

        Returns:
            int. The total Exp of the Clan.
        """
        return sum(int(row[2]) for row in clan_list[1:])

    def __repr__(self) -> str:
        return f"Clan(name={repr(self.name)}, exp={self.exp}, avg_exp={self.avg_exp}, count={self.count})"

    def __iter__(self) -> ClanMember:
        """

        Iterates through `self.member` dict attribute, if `set_dict` was passed True when instancing `Clan` object.

        Yields:
            ClanMember. ClanMember object of each member in the clan::
                >>> import rs3clans
                >>> clan = rs3clans.Clan('atlantis')
                >>> for member in clan:
                ...     print(f"{member} - {member.name}")
                ...
                ClanMember(Pedim, Owner, 1249520826) - Pedim
                ClanMember(Acriano, Overseer, 1903276564) - Acriano
                ClanMember(Cogu, Overseer, 1829449412) - Cogu
                ClanMember(Black bullet, Overseer, 1100767386) - Black Bullet
                ClanMember(NRiver, Overseer, 1090093362) - NRiver
                ClanMember(Kurenaii, Overseer, 395850997) - Kurenaii
                (...)
        """
        if self.member:
            for key, value in self.member.items():
                yield value
