from enum import Enum


class SCORE(Enum):
    LOVE = 0
    FIFTEEN = 1
    THIRTY = 2
    FORTY = 3
    GAME = 4


class TennisGame:
    def __init__(self, player1_name, player2_name):
        self.player1_name = player1_name
        self.player2_name = player2_name
        self.player1_points = 0
        self.player2_points = 0

    def won_point(self, player_name):
        if player_name == self.player1_name:
            self.player1_points = self.player1_points + 1
        else:
            self.player2_points = self.player2_points + 1

    def _get_even_points_score(self):
        if self.player1_points == SCORE.LOVE.value:
            return "Love-All"
        if self.player1_points == SCORE.FIFTEEN.value:
            return "Fifteen-All"
        if self.player1_points == SCORE.THIRTY.value:
            return "Thirty-All"

        return "Deuce"

    def _get_beyond_deuce_score(self):
        points_difference = self.player1_points - self.player2_points

        if points_difference == 1:
            return f"Advantage {self.player1_name}"
        if points_difference == -1:
            return f"Advantage {self.player2_name}"
        if points_difference >= 2:
            return f"Win for {self.player1_name}"

        return f"Win for {self.player2_name}"

    def _get_score_name(self, points):
        if points == SCORE.LOVE.value:
            return "Love"
        if points == SCORE.FIFTEEN.value:
            return "Fifteen"
        if points == SCORE.THIRTY.value:
            return "Thirty"

        return "Forty"

    def _get_before_deuce_score(self):
        player1_score = self._get_score_name(self.player1_points)
        player2_score = self._get_score_name(self.player2_points)
        return f"{player1_score}-{player2_score}"

    def get_score(self):
        if self.player1_points == self.player2_points:
            return self._get_even_points_score()

        if self.player1_points >= SCORE.GAME.value or self.player2_points >= SCORE.GAME.value:
            return self._get_beyond_deuce_score()

        return self._get_before_deuce_score()
