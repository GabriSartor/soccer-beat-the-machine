import unittest
import sys
sys.path.append('../src/entities/')

from league import League
from area import Area
from match import Match
from player import Player
from season import Season
from team import Team

import json

class TestLeague(unittest.TestCase):

    def test_equality(self):
        league_1 = None
        with open('../models/league.json', 'r') as file:
            data = file.read()
            deserialized_data = json.loads(data)
            league_1 = League.fromJson(data)

        league_2 = League(2019, "Serie A", "SA", "TIER_ONE", 638, 2114)

        self.assertEqual(league_1, league_2)

unittest.main()