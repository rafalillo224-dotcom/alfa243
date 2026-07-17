from alfa243.domain.match_analysis import MatchAnalysis
from alfa243.domain.match_data import MatchData
from alfa243.services.match_analyzer import MatchAnalyzer


class RoundAnalyzer:
    """Analiza una colección completa de partidos."""

    def __init__(
        self,
        match_analyzer: MatchAnalyzer,
    ) -> None:
        self.match_analyzer = match_analyzer

    def analyze(
        self,
        matches: list[MatchData],
    ) -> list[MatchAnalysis]:
        ordered_matches = sorted(
            matches,
            key=lambda match: match.kickoff,
        )

        return [
            self.match_analyzer.analyze(match)
            for match in ordered_matches
        ]