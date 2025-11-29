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

    def get_even_points_score(self):
        if self.player1_points == SCORE.LOVE.value:
            return "Love-All"
        if self.player1_points == SCORE.FIFTEEN.value:
            return "Fifteen-All"
        if self.player1_points == SCORE.THIRTY.value:
            return "Thirty-All"

        return "Deuce"

    def get_beyond_deuce_score(self):
        points_difference = self.player1_points - self.player2_points

        if points_difference == 1:
            return f"Advantage {self.player1_name}"
        if points_difference == -1:
            return f"Advantage {self.player2_name}"
        if points_difference >= 2:
            return f"Win for {self.player1_name}"

        return f"Win for {self.player2_name}"

    def get_before_deuce_score(self, score):
        temp_score = 0
        for i in range(SCORE.FIFTEEN.value, SCORE.FORTY.value):
            if i == 1:
                temp_score = self.player1_points
            else:
                score = score + "-"
                temp_score = self.player2_points

            if temp_score == SCORE.LOVE.value:
                score = score + "Love"
            elif temp_score == SCORE.FIFTEEN.value:
                score = score + "Fifteen"
            elif temp_score == SCORE.THIRTY.value:
                score = score + "Thirty"
            elif temp_score == SCORE.FORTY.value:
                score = score + "Forty"

        return score

    def get_score(self):
        score = ""

        if self.player1_points == self.player2_points:
            return self.get_even_points_score()

        if self.player1_points >= SCORE.GAME.value or self.player2_points >= SCORE.GAME.value:
            return self.get_beyond_deuce_score()

        return self.get_before_deuce_score(score)
