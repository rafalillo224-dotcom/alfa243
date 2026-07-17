from alfa243.domain.match import Match
from alfa243.domain.match_analysis import MatchAnalysis
from alfa243.domain.match_data import MatchData
from alfa243.engines.expected_goals import ExpectedGoalsEngine
from alfa243.engines.fusion import FusionEngine
from alfa243.engines.market import MarketEngine
from alfa243.engines.poisson import PoissonEngine
from alfa243.repositories.team_repository import TeamRepository
from alfa243.services.match_statistics import MatchStatistics


class MatchAnalyzer:
    """Coordina todos los motores necesarios para analizar un partido."""

    def __init__(
        self,
        team_repository: TeamRepository,
        market_weight: float = 0.50,
        poisson_weight: float = 0.50,
        top_scores_limit: int = 5,
    ) -> None:
        if market_weight < 0 or poisson_weight < 0:
            raise ValueError("Los pesos no pueden ser negativos.")

        if market_weight + poisson_weight <= 0:
            raise ValueError(
                "La suma de los pesos debe ser mayor que cero."
            )

        if top_scores_limit <= 0:
            raise ValueError(
                "El límite de marcadores debe ser mayor que cero."
            )

        self.team_repository = team_repository
        self.market_weight = market_weight
        self.poisson_weight = poisson_weight
        self.top_scores_limit = top_scores_limit

        self.market_engine = MarketEngine()
        self.poisson_engine = PoissonEngine()

    def analyze(
        self,
        match_data: MatchData,
    ) -> MatchAnalysis:
        home_statistics = self.team_repository.get(
            match_data.home_team
        )

        away_statistics = self.team_repository.get(
            match_data.away_team
        )

        home_xg, away_xg = ExpectedGoalsEngine.calculate(
            home_statistics,
            away_statistics,
        )

        market_match = Match(
            home_team=match_data.home_team,
            away_team=match_data.away_team,
            home_odds=match_data.home_odds,
            draw_odds=match_data.draw_odds,
            away_odds=match_data.away_odds,
        )

        market_prediction = self.market_engine.predict(
            market_match
        )

        poisson_prediction = self.poisson_engine.predict(
            home_expected_goals=home_xg,
            away_expected_goals=away_xg,
        )

        fusion_prediction = FusionEngine.predict(
            market_prediction,
            poisson_prediction,
            first_weight=self.market_weight,
            second_weight=self.poisson_weight,
        )

        matrix = self.poisson_engine.score_matrix(
            home_expected_goals=home_xg,
            away_expected_goals=away_xg,
        )

        top_scores = MatchStatistics.top_scores(
            matrix,
            limit=self.top_scores_limit,
        )

        return MatchAnalysis(
            match=match_data,
            home_expected_goals=home_xg,
            away_expected_goals=away_xg,
            market_prediction=market_prediction,
            poisson_prediction=poisson_prediction,
            fusion_prediction=fusion_prediction,
            btts=MatchStatistics.btts(matrix),
            over_25=MatchStatistics.over_25(matrix),
            under_25=MatchStatistics.under_25(matrix),
            top_scores=tuple(top_scores),
        )