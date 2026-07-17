from alfa243.domain.match import Match
from alfa243.domain.prediction import Prediction
from alfa243.domain.score_probability import ScoreProbability


def show_prediction(
    match: Match,
    market: Prediction,
    poisson: Prediction,
    top_scores: list[ScoreProbability],
) -> None:

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
    print("=== Top 5 marcadores ===")

    for index, score in enumerate(top_scores, start=1):
        print(
            f"{index}. "
            f"{score.home_goals}-{score.away_goals}   "
            f"{score.probability:.2%}"
        )