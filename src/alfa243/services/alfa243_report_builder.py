from math import isinf

from alfa243.domain.alfa243_result import Alfa243Result
from alfa243.domain.classified_match import ClassifiedMatch
from alfa243.domain.combination_analysis import CombinationAnalysis


class Alfa243ReportBuilder:
    """Construye informes de texto a partir de un resultado ALFA-243."""

    def build(
        self,
        result: Alfa243Result,
        top_limit: int = 10,
    ) -> str:
        if top_limit <= 0:
            raise ValueError(
                "El límite del ranking debe ser positivo."
            )

        lines: list[str] = []

        lines.extend(self._build_header(result))
        lines.append("")
        lines.extend(self._build_summary(result))
        lines.append("")
        lines.extend(self._build_favorites(result))
        lines.append("")
        lines.extend(self._build_balanced(result))
        lines.append("")
        lines.extend(
            self._build_ranking(
                result=result,
                top_limit=top_limit,
            )
        )

        return "\n".join(lines)

    @staticmethod
    def _build_header(
        result: Alfa243Result,
    ) -> list[str]:
        separator = "=" * 64

        return [
            separator,
            "ALFA-243".center(64),
            separator,
            f"Competición : {result.competition}",
            f"Temporada   : {result.season}",
            f"Jornada     : {result.round_number}",
        ]

    @staticmethod
    def _build_summary(
        result: Alfa243Result,
    ) -> list[str]:
        return [
            "-" * 64,
            "RESUMEN",
            "-" * 64,
            (
                "Partidos analizados ............ "
                f"{result.analyzed_match_count}"
            ),
            (
                "Favoritos seleccionados ........ "
                f"{len(result.selection.favorites)}"
            ),
            (
                "Igualados seleccionados ........ "
                f"{len(result.selection.balanced)}"
            ),
            (
                "Patrones válidos ............... "
                f"{result.valid_pattern_count}"
            ),
            (
                "Combinaciones seleccionadas .... "
                f"{result.selected_combination_count}"
            ),
            (
                "Cobertura del universo válido .. "
                f"{result.coverage_percent:.2f} %"
            ),
        ]

    def _build_favorites(
        self,
        result: Alfa243Result,
    ) -> list[str]:
        lines = [
            "-" * 64,
            "6 FAVORITOS",
            "-" * 64,
        ]

        for position, classified in enumerate(
            result.selection.favorites,
            start=1,
        ):
            lines.append(
                self._format_classified_match(
                    position=position,
                    classified=classified,
                )
            )

        return lines

    def _build_balanced(
        self,
        result: Alfa243Result,
    ) -> list[str]:
        lines = [
            "-" * 64,
            "6 IGUALADOS",
            "-" * 64,
        ]

        for position, classified in enumerate(
            result.selection.balanced,
            start=1,
        ):
            lines.append(
                self._format_classified_match(
                    position=position,
                    classified=classified,
                )
            )

        return lines

    @staticmethod
    def _format_classified_match(
        position: int,
        classified: ClassifiedMatch,
    ) -> str:
        match = classified.analysis.match

        return (
            f"{position:>2}. "
            f"{match.home_team} vs {match.away_team} | "
            f"Signo: {classified.selected_outcome} | "
            f"Prob.: {classified.selected_probability * 100:.2f} % | "
            f"Gap: {classified.probability_gap * 100:.2f} pp"
        )

    def _build_ranking(
        self,
        result: Alfa243Result,
        top_limit: int,
    ) -> list[str]:
        available = len(result.portfolio.analyses)
        displayed = min(top_limit, available)

        lines = [
            "-" * 64,
            f"TOP {displayed} COMBINACIONES",
            "-" * 64,
        ]

        for analysis in result.portfolio.analyses[:displayed]:
            lines.extend(
                self._format_combination_analysis(analysis)
            )

        return lines

    @staticmethod
    def _format_combination_analysis(
        analysis: CombinationAnalysis,
    ) -> list[str]:
        if isinf(analysis.fair_odds):
            fair_odds = "∞"
        else:
            fair_odds = f"{analysis.fair_odds:.2f}"

        return [
            (
                f"#{analysis.rank:<3} "
                f"Código: {analysis.code} | "
                f"1: {analysis.home_count} | "
                f"X: {analysis.draw_count} | "
                f"2: {analysis.away_count}"
            ),
            (
                "     "
                f"Probabilidad: {analysis.probability_percent:.6f} % | "
                f"Cuota justa: {fair_odds} | "
                "Cobertura acumulada: "
                f"{analysis.cumulative_coverage * 100:.2f} %"
            ),
        ]