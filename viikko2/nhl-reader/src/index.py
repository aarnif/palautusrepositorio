from rich.console import Console
from rich.table import Table
from player_reader import PlayerReader
from player_stats import PlayerStats

SEASONS = ["2018-19", "2019-20", "2020-21", "2021-22",
           "2022-23", "2023-24", "2024-25", "2025-26"]
NATIONALITIES = ["RUS", "FIN", "DEN", "CAN", "BLR", "NOR", "GER", "SLO", "SWE",
                 "LAT", "NED", "CZE", "SVK", "UZB", "SUI", "GBR", "AUT", "USA", "AUS", "FRA"]


def display_players(players, season, nationality):
    console = Console()
    table = Table(title=f"Season {season} players from {nationality}")

    table.add_column("Name", style="cyan")
    table.add_column("Provides", style="magenta")
    table.add_column("Goals", justify="right", style="green")
    table.add_column("Assists", justify="right", style="green")
    table.add_column("Points", justify="right", style="green")

    for player in players:
        table.add_row(
            player.name,
            player.team,
            str(player.goals),
            str(player.assists),
            str(player.points)
        )

    console.print(table)


def get_season(seasons):
    while True:
        season = input(
            "Season [2018-19/2019-20/2020-21/2021-22/2022-23/2023-24/2024-25/2025-26] (2024-25): ")
        if season in seasons:
            return season
        print("Please provide a valid season.")


def get_nationality(season):
    while True:
        nationality = input(
            "Nationality "
            "[RUS/FIN/DEN/CAN/BLR/NOR/GER/SLO/SWE/LAT/NED/CZE/SVK/UZB/SUI/GBR/AUT/USA/AUS/FRA] ():")

        if nationality in NATIONALITIES:
            url = f"https://studies.cs.helsinki.fi/nhlstats/{season}/players"
            reader = PlayerReader(url)
            stats = PlayerStats(reader)
            players = stats.top_scorers_by_nationality(nationality)
            display_players(players, season, nationality)
        else:
            print("Please provide a valid nationality.")


def main():
    season = get_season(SEASONS)
    get_nationality(season)


if __name__ == "__main__":
    main()
