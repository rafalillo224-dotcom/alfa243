from alfa243.domain.score_probability import ScoreProbability


class MatchStatistics:

    @staticmethod
    def most_likely_score(
        matrix: list[ScoreProbability],
    ) -> ScoreProbability:
        return max(matrix, key=lambda score: score.probability)