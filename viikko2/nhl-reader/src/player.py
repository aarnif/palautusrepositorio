class Player:
    def __init__(self, dict):
        self.name = dict['name']
        self.team = dict['team']
        self.nationality = dict['nationality']
        self.assists = dict['assists']
        self.goals = dict['goals']
        self.games = dict['games']

    def __str__(self):
        return f"{self.name:24} {self.team:16} {self.goals} + {self.assists} = {self.goals + self.assists}"
