import requests
from player import Player


class PlayerReader:
    def __init__(self, url):
        self.url = url

    def read(self):
        return requests.get(self.url, timeout=5).json()

    def get_players(self):
        response = self.read()

        return [Player(player_dict) for player_dict in response]
