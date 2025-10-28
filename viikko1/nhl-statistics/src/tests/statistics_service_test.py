import unittest
from statistics_service import StatisticsService, SortBy
from player import Player

class PlayerReaderStub:
    def get_players(self):
        return [
            Player("Semenko", "EDM", 4, 12),  #  4+12 = 16
            Player("Lemieux", "PIT", 45, 54), # 45+54 = 99
            Player("Kurri",   "EDM", 37, 53), # 37+53 = 90
            Player("Yzerman", "DET", 42, 56), # 42+56 = 98
            Player("Gretzky", "EDM", 35, 89)  # 35+89 = 124
        ]

class TestStatisticsService(unittest.TestCase):
    def setUp(self):
        # annetaan StatisticsService-luokan oliolle "stub"-luokan olio
        self.stats = StatisticsService(
            PlayerReaderStub()
        )

    def test_searches_for_a_player(self):
        player = self.stats.search("Semenko")
        self.assertEqual(player.name, "Semenko")
        self.assertEqual(player.team, "EDM")
        self.assertEqual(player.goals, 4)
        self.assertEqual(player.assists, 12)

    def test_returns_none_with_non_existent_player(self):
        player = self.stats.search("Virtanen")
        self.assertEqual(player, None)

    def test_returns_team_members(self):
        team = self.stats.team("EDM")
        self.assertEqual(len(team), 3)

        for player in team:
            self.assertEqual(player.team, "EDM")

    def test_uses_sortby_points_as_default(self):
        ranking = self.stats.top(3)
        self.assertEqual(len(ranking), 4)

        top_player = ranking[0]

        self.assertEqual(top_player.name, "Gretzky")
        self.assertEqual(top_player.team, "EDM")
        self.assertEqual(top_player.goals, 35)
        self.assertEqual(top_player.assists, 89)

    def test_returns_top_player_by_points(self):
        ranking = self.stats.top(3, SortBy.POINTS)
        self.assertEqual(len(ranking), 4)

        top_player = ranking[0]

        self.assertEqual(top_player.name, "Gretzky")
        self.assertEqual(top_player.team, "EDM")
        self.assertEqual(top_player.goals, 35)
        self.assertEqual(top_player.assists, 89)

    def test_returns_top_player_by_goals(self):
        ranking = self.stats.top(3, SortBy.GOALS)
        self.assertEqual(len(ranking), 4)

        top_player = ranking[0]

        self.assertEqual(top_player.name, "Lemieux")
        self.assertEqual(top_player.team, "PIT")
        self.assertEqual(top_player.goals, 45)
        self.assertEqual(top_player.assists, 54)

    def test_returns_top_player_by_assists(self):
        ranking = self.stats.top(3, SortBy.ASSISTS)
        self.assertEqual(len(ranking), 4)

        top_player = ranking[0]

        self.assertEqual(top_player.name, "Gretzky")
        self.assertEqual(top_player.team, "EDM")
        self.assertEqual(top_player.goals, 35)
        self.assertEqual(top_player.assists, 89)