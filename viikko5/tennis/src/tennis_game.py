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

    def get_even_points_score(self, score):
        if self.player1_points == 0:
            score = "Love-All"
        elif self.player1_points == 1:
            score = "Fifteen-All"
        elif self.player1_points == 2:
            score = "Thirty-All"
        else:
            score = "Deuce"
        return score

    def get_beyond_deuce_score(self, score):
        minus_result = self.player1_points - self. player2_points

        if minus_result == 1:
            score = "Advantage player1"
        elif minus_result == -1:
            score = "Advantage player2"
        elif minus_result >= 2:
            score = "Win for player1"
        else:
            score = "Win for player2"

        return score

    def get_before_deuce_score(self, score):
        temp_score = 0
        for i in range(1, 3):
            if i == 1:
                temp_score = self.player1_points
            else:
                score = score + "-"
                temp_score = self.player2_points

            if temp_score == 0:
                score = score + "Love"
            elif temp_score == 1:
                score = score + "Fifteen"
            elif temp_score == 2:
                score = score + "Thirty"
            elif temp_score == 3:
                score = score + "Forty"

        return score

    def get_score(self):
        score = ""

        if self.player1_points == self.player2_points:
            return self.get_even_points_score(score)

        if self.player1_points >= 4 or self.player2_points >= 4:
            return self.get_beyond_deuce_score(score)

        return self.get_before_deuce_score(score)
