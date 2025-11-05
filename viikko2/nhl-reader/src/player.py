class Player:
    def __init__(self, player_dict):
        self.name = player_dict['name']
        self.team = player_dict['team']
        self.nationality = player_dict['nationality']
        self.assists = player_dict['assists']
        self.goals = player_dict['goals']
        self.games = player_dict['games']
        self.points = self.get_points()

    def get_points(self):
        return self.goals + self.assists

    def __str__(self):
        return f"{self.name:24} {self.team:16} {self.goals} + {self.assists} = {self.points}"
