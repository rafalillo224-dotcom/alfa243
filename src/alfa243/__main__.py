from alfa243.cli.console import show_prediction
from alfa243.domain.match import Match
from alfa243.engines.fusion import FusionEngine
from alfa243.engines.market import MarketEngine
from alfa243.engines.poisson import PoissonEngine
from alfa243.services.match_statistics import MatchStatistics
from alfa243.version import __version__


def main() -> None:

    print("====================================")
    print(f"ALFA-243 v{__version__}")
    print("====================================")

    match = Match(
        home_team="Real Madrid",
        away_team="Barcelona",
        home_odds=2.10,
        draw_odds=3.40,
        away_odds=3.20,
    )

    print("\nPartido:")
    print(f"{match.home_team} vs {match.away_team}")

    market_prediction = MarketEngine().predict(match)

    poisson_engine = PoissonEngine()

    poisson_prediction = poisson_engine.predict(
        home_expected_goals=1.8,
        away_expected_goals=1.1,
    )

    fusion_prediction = FusionEngine.predict(
        market_prediction,
        poisson_prediction,
        first_weight=0.50,
        second_weight=0.50,
    )

    matrix = poisson_engine.score_matrix(
        home_expected_goals=1.8,
        away_expected_goals=1.1,
    )

    top_scores = MatchStatistics.top_scores(
        matrix,
        limit=5,
    )

    btts = MatchStatistics.btts(matrix)
    over_25 = MatchStatistics.over_25(matrix)
    under_25 = MatchStatistics.under_25(matrix)

    show_prediction(
        market=market_prediction,
        poisson=poisson_prediction,
        fusion=fusion_prediction,
        top_scores=top_scores,
        btts=btts,
        over_25=over_25,
        under_25=under_25,
    )


if __name__ == "__main__":
    main()