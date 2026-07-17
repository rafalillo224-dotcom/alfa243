from unittest.mock import Mock

from alfa243.cli.console_renderer import ConsoleRenderer


def test_renderer_builds_and_prints_report() -> None:
    builder = Mock()
    output = Mock()
    result = Mock()

    builder.build.return_value = "Informe ALFA-243"

    renderer = ConsoleRenderer(
        report_builder=builder,
        output=output,
    )

    report = renderer.render(
        result=result,
        top_limit=5,
    )

    builder.build.assert_called_once_with(
        result=result,
        top_limit=5,
    )

    output.assert_called_once_with(
        "Informe ALFA-243"
    )

    assert report == "Informe ALFA-243"