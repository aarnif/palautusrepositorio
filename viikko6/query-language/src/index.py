from statistics import Statistics
from player_reader import PlayerReader
from matchers import And, Not, All, HasAtLeast, PlaysIn, HasFewerThan


def main():
    url = "https://studies.cs.helsinki.fi/nhlstats/2024-25/players.txt"
    reader = PlayerReader(url)
    stats = Statistics(reader)

    # matcher = And(
    #     HasAtLeast(5, "goals"),
    #     HasAtLeast(20, "assists"),
    #     PlaysIn("PHI")
    # )

    matcher = And(
        Not(HasAtLeast(2, "goals")),
        PlaysIn("NYR")
    )

    for player in stats.matches(matcher):
        print(player)

    matcher = And(
        HasFewerThan(2, "goals"),
        PlaysIn("NYR")
    )

    print()

    for player in stats.matches(matcher):
        print(player)

    filtered_with_all = stats.matches(All())
    print(len(filtered_with_all))  # 899


if __name__ == "__main__":
    main()
