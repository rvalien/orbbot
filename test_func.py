import unittest
from moduls import get_random_spectators_and_players
import logging

logger = logging.getLogger(__name__)

PLAYERS = ["player01", "player02", "player03", "player04", "player05", "player06", "player07", "player08", "player09"]


class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(len(PLAYERS), 9)

    def test_get_random_spectators_and_players_more_8(self):
        players, spectators = get_random_spectators_and_players(PLAYERS)  # 9
        self.assertEqual(len(players), 8)
        self.assertEqual(len(spectators), 1)

    def test_get_random_spectators_and_players_eq_8(self):
        players, spectators = get_random_spectators_and_players(PLAYERS[:8])  # 8
        self.assertEqual(len(players), 8)
        self.assertEqual(len(spectators), 0)

    def test_get_random_spectators_and_players_le_8(self):
        players, spectators = get_random_spectators_and_players(PLAYERS[:5])  # 5
        self.assertEqual(len(players), 4)
        self.assertEqual(len(spectators), 1)


if __name__ == "__main__":
    unittest.main()
