import requests
from player import Player

def main():
    url = "https://studies.cs.helsinki.fi/nhlstats/2024-25/players"
    response = requests.get(url).json()
    players = []

    for player_dict in response:
        player = Player(player_dict)
        players.append(player)

    print("Players from FIN")
    print()

    finnish_players = list(filter(lambda player: player.nationality == "FIN", players))

    for player in sorted(finnish_players, reverse=True, key=lambda player: player.goals + player.assists):
        print(player)


if __name__ == "__main__":
    main()
