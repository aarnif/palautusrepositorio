class PlayerStats:
    def __init__(self, reader):
        self.reader = reader

    def players_by_nationality(self, nationality):
        players = self.reader.get_players()
        return [player for player in players if player.nationality == nationality]

    def top_scorers_by_nationality(self, nationality):
        players_by_nationality = self.players_by_nationality(nationality)
        return sorted(players_by_nationality, reverse=True, key=lambda player: player.points)
