from alfa243.domain.alfa243_result import Alfa243Result
from alfa243.domain.match_data import MatchData
from alfa243.repositories.match_repository import MatchRepository
from alfa243.services.alfa_selector import AlfaSelector
from alfa243.services.combination_analyzer import CombinationAnalyzer
from alfa243.services.combination_generator import CombinationGenerator
from alfa243.services.match_classifier import MatchClassifier
from alfa243.services.round_analyzer import RoundAnalyzer


class Alfa243Engine:
    """Coordina el pipeline completo del sistema ALFA-243."""

    def __init__(
        self,
        match_repository: MatchRepository,
        round_analyzer: RoundAnalyzer,
        match_classifier: MatchClassifier,
        alfa_selector: AlfaSelector,
        combination_generator: CombinationGenerator,
        combination_analyzer: CombinationAnalyzer,
    ) -> None:
        self.match_repository = match_repository
        self.round_analyzer = round_analyzer
        self.match_classifier = match_classifier
        self.alfa_selector = alfa_selector
        self.combination_generator = combination_generator
        self.combination_analyzer = combination_analyzer

    def analyze_round(
        self,
        competition: str,
        season: str,
        round_number: int,
    ) -> Alfa243Result:
        """Carga y analiza una jornada desde el repositorio."""

        self._validate_round_arguments(
            competition=competition,
            season=season,
            round_number=round_number,
        )

        matches = self.match_repository.get_by_round(
            competition=competition,
            season=season,
            round_number=round_number,
        )

        if not matches:
            raise ValueError(
                "No se encontraron partidos para "
                f"{competition}, {season}, jornada {round_number}."
            )

        return self.analyze_matches(
            matches=matches,
            competition=competition,
            season=season,
            round_number=round_number,
        )

    def analyze_matches(
        self,
        matches: list[MatchData],
        competition: str,
        season: str,
        round_number: int,
    ) -> Alfa243Result:
        """Ejecuta el pipeline sobre una lista de partidos."""

        self._validate_round_arguments(
            competition=competition,
            season=season,
            round_number=round_number,
        )

        if not matches:
            raise ValueError(
                "Debe existir al menos un partido para analizar."
            )

        match_analyses = self.round_analyzer.analyze(matches)

        classified_matches = self.match_classifier.classify_all(
            match_analyses
        )

        selection = self.alfa_selector.select(
            classified_matches
        )

        selected_combinations = (
            self.combination_generator.generate(selection)
        )

        valid_universe = (
            self.combination_generator.generate_all(selection)
        )

        portfolio = self.combination_analyzer.analyze(
            selected=selected_combinations,
            valid_universe=valid_universe,
        )

        return Alfa243Result(
            competition=competition,
            season=season,
            round_number=round_number,
            match_analyses=tuple(match_analyses),
            selection=selection,
            portfolio=portfolio,
            valid_pattern_count=len(valid_universe),
        )

    @staticmethod
    def _validate_round_arguments(
        competition: str,
        season: str,
        round_number: int,
    ) -> None:
        if not competition.strip():
            raise ValueError(
                "La competición no puede estar vacía."
            )

        if not season.strip():
            raise ValueError(
                "La temporada no puede estar vacía."
            )

        if round_number <= 0:
            raise ValueError(
                "El número de jornada debe ser positivo."
            )