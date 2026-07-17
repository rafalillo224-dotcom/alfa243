from alfa243.domain.team_statistics import TeamStatistics


class ExpectedGoalsEngine:
    """Calcula goles esperados a partir de estadísticas de dos equipos."""

    @staticmethod
    def calculate(
        home_statistics: TeamStatistics,
        away_statistics: TeamStatistics,
    ) -> tuple[float, float]:

        home_expected_goals = (
            home_statistics.goals_for
            + away_statistics.goals_against
        ) / 2

        away_expected_goals = (
            away_statistics.goals_for
            + home_statistics.goals_against
        ) / 2

        return home_expected_goals, away_expected_goals