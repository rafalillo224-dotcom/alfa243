from alfa243.domain.prediction import Prediction
from alfa243.domain.score_probability import ScoreProbability


def show_prediction(
    market: Prediction,
    poisson: Prediction,
    fusion: Prediction,
    top_scores: list[ScoreProbability],
    btts: float,
    over_25: float,
    under_25: float,
) -> None:

    print("\n=== Mercado ===\n")
    _show_probabilities(market)

    print("\n=== Poisson ===\n")
    _show_probabilities(poisson)

    print("\n=== Fusión ===\n")
    _show_probabilities(fusion)

    print("\n=== Mercados de goles ===\n")
    print(f"BTTS        {btts:.2%}")
    print(f"Over 2.5    {over_25:.2%}")
    print(f"Under 2.5   {under_25:.2%}")

    print("\n=== Marcadores más probables ===\n")

    for score in top_scores:
        print(
            f"{score.home_goals}-{score.away_goals} "
            f"({score.probability:.2%})"
        )


def _show_probabilities(prediction: Prediction) -> None:

    print(f"Local      {prediction.home:.2%}")
    print(f"Empate     {prediction.draw:.2%}")
    print(f"Visitante  {prediction.away:.2%}")