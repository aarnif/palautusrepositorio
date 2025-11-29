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
        self.player1_score = 0
        self.player2_score = 0

    def won_point(self, player_name):
        if player_name == self.player1_name:
            self.player1_score = self.player1_score + 1
        else:
            self.player2_score = self.player2_score + 1

    def _get_tied_score(self):
        if self.player1_score == SCORE.LOVE.value:
            return "Love-All"
        if self.player1_score == SCORE.FIFTEEN.value:
            return "Fifteen-All"
        if self.player1_score == SCORE.THIRTY.value:
            return "Thirty-All"
        return "Deuce"

    def _get_advantage_or_win_score(self):
        score_difference = self.player1_score - self.player2_score

        if score_difference == 1:
            return f"Advantage {self.player1_name}"
        if score_difference == -1:
            return f"Advantage {self.player2_name}"
        if score_difference >= 2:
            return f"Win for {self.player1_name}"
        return f"Win for {self.player2_name}"

    def _point_to_score_name(self, points):
        if points == SCORE.LOVE.value:
            return "Love"
        if points == SCORE.FIFTEEN.value:
            return "Fifteen"
        if points == SCORE.THIRTY.value:
            return "Thirty"
        return "Forty"

    def _get_uneven_score(self):
        player1_score_name = self._point_to_score_name(self.player1_score)
        player2_score_name = self._point_to_score_name(self.player2_score)
        return f"{player1_score_name}-{player2_score_name}"

    def get_score(self):
        if self.player1_score == self.player2_score:
            return self._get_tied_score()

        if self.player1_score >= SCORE.GAME.value or self.player2_score >= SCORE.GAME.value:
            return self._get_advantage_or_win_score()

        return self._get_uneven_score()
