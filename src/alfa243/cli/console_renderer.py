from collections.abc import Callable

from alfa243.domain.alfa243_result import Alfa243Result
from alfa243.services.alfa243_report_builder import (
    Alfa243ReportBuilder,
)


class ConsoleRenderer:
    """Muestra informes ALFA-243 en la consola."""

    def __init__(
        self,
        report_builder: Alfa243ReportBuilder,
        output: Callable[[str], None] = print,
    ) -> None:
        self.report_builder = report_builder
        self.output = output

    def render(
        self,
        result: Alfa243Result,
        top_limit: int = 10,
    ) -> str:
        report = self.report_builder.build(
            result=result,
            top_limit=top_limit,
        )

        self.output(report)

        return report