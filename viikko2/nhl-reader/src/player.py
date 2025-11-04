class Player:
    def __init__(self, dict):
        self.name = dict['name']
        self.team = dict['team']
        self.nationality = dict['nationality']
        self.assists = dict['assists']
        self.goals = dict['goals']
        self.games = dict['games']

    def __str__(self):
        return f"{self.name} team {self.team} goals {self.goals} assists {self.assists}"
