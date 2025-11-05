class PlayerStats:
    def __init__(self, reader):
        self.reader = reader
    
    def top_scorers_by_nationality(self, nationality):
        players = self.reader.get_players()

        players_by_nationality = list(filter(lambda player: player.nationality == nationality, players))

        return sorted(players_by_nationality, reverse=True, key=lambda player: player.points)
        
