from alfa243.domain.score_probability import ScoreProbability


class MatchStatistics:

    @staticmethod
    def most_likely_score(
        matrix: list[ScoreProbability],
    ) -> ScoreProbability:

        return max(
            matrix,
            key=lambda score: score.probability,
        )

    @staticmethod
    def top_scores(
        matrix: list[ScoreProbability],
        limit: int = 5,
    ) -> list[ScoreProbability]:

        return sorted(
            matrix,
            key=lambda score: score.probability,
            reverse=True,
        )[:limit]

    @staticmethod
    def btts(
        matrix: list[ScoreProbability],
    ) -> float:

        return sum(
            score.probability
            for score in matrix
            if score.home_goals > 0
            and score.away_goals > 0
        )

    @staticmethod
    def over_25(
        matrix: list[ScoreProbability],
    ) -> float:

        return sum(
            score.probability
            for score in matrix
            if score.home_goals + score.away_goals >= 3
        )

    @staticmethod
    def under_25(
        matrix: list[ScoreProbability],
    ) -> float:

        return 1.0 - MatchStatistics.over_25(matrix)