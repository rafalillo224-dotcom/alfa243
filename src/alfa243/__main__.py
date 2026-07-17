from alfa243.cli.console import show_prediction
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

    poisson_engine = PoissonEngine()

    poisson = poisson_engine.predict(
        home_expected_goals=1.80,
        away_expected_goals=1.10,
    )

    matrix = poisson_engine.score_matrix(
        home_expected_goals=1.80,
        away_expected_goals=1.10,
    )

    top_scores = MatchStatistics.top_scores(matrix)

    show_prediction(
        match=match,
        market=market,
        poisson=poisson,
        top_scores=top_scores,
    )


if __name__ == "__main__":
    main()