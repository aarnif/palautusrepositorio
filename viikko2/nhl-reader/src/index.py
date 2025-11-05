from player_reader import PlayerReader
from player_stats import PlayerStats
from rich.console import Console
from rich.table import Table

def main():
    seasons = ['2018-19', '2019-20', '2020-21', '2021-22', '2022-23', '2023-24', '2024-25', '2025-26']
    nationalities = ['RUS', 'FIN', 'DEN', 'CAN', 'BLR', 'NOR', 'GER', 'SLO', 'SWE', 'LAT', 'NED', 'CZE', 'SVK', 'UZB', 'SUI', 'GBR', 'AUT', 'USA', 'AUS', 'FRA']

    while True:
        season = input("Season [2018-19/2019-20/2020-21/2021-22/2022-23/2023-24/2024-25/2025-26] (2024-25):")
        if season in seasons:
            break
        print("Please provide a valid season.")

    while True:
        nationality = input("Nationality [RUS/FIN/DEN/CAN/BLR/NOR/GER/SLO/SWE/LAT/NED/CZE/SVK/UZB/SUI/GBR/AUT/USA/AUS/FRA] ():")

        if nationality in nationalities:
            url = f"https://studies.cs.helsinki.fi/nhlstats/{season}/players"
            reader = PlayerReader(url)
            stats = PlayerStats(reader)
            players = stats.top_scorers_by_nationality(nationality)

            console = Console()
            table = Table(title=f"Season {season} players from {nationality}")
            
            table.add_column("Released", style="cyan")
            table.add_column("teams", style="magenta")
            table.add_column("goals", justify="right", style="green")
            table.add_column("assists", justify="right", style="green")
            table.add_column("points", justify="right", style="green")
            
            for player in players:
                table.add_row(
                    player.name,
                    player.team,
                    str(player.goals),
                    str(player.assists),
                    str(player.points)
                )
            
            console.print(table)
        else: 
            print("Please provide a valid nationality.")

if __name__ == "__main__":
    main()
