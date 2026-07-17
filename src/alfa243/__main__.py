from alfa243.core.kernel import run

from alfa243.domain.match import Match
from alfa243.engines.market import MarketEngine
from alfa243.engines.poisson import PoissonEngine
from alfa243.services.match_statistics import MatchStatistics


def main():
    run()

    match = Match(
        home_team="Real Madrid",
        away_team="Barcelona",
        home_odds=2.10,
        draw_odds=3.40,
        away_odds=3.20,
    )

    market = MarketEngine().predict(match)

    poisson = PoissonEngine().predict(
        home_expected_goals=1.80,
        away_expected_goals=1.10,
    )

    matrix = PoissonEngine.score_matrix(
        home_expected_goals=1.80,
        away_expected_goals=1.10,
    )

    score = MatchStatistics.most_likely_score(matrix)

    print()
    print(f"Partido: {match.home_team} vs {match.away_team}")

    print()
    print("=== Mercado ===")
    print(f"Local      {market.home:.2%}")
    print(f"Empate     {market.draw:.2%}")
    print(f"Visitante  {market.away:.2%}")

    print()
    print("=== Poisson ===")
    print(f"Local      {poisson.home:.2%}")
    print(f"Empate     {poisson.draw:.2%}")
    print(f"Visitante  {poisson.away:.2%}")

    print()
    print("=== Marcador más probable ===")
    print(
        f"{score.home_goals}-{score.away_goals} "
        f"({score.probability:.2%})"
    )


if __name__ == "__main__":
    main()