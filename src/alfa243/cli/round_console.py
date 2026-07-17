from alfa243.domain.match_analysis import MatchAnalysis


def show_round_analysis(
    analyses: list[MatchAnalysis],
) -> None:
    if not analyses:
        print("\nNo se encontraron partidos para analizar.")
        return

    first_match = analyses[0].match

    print("\n====================================")
    print(
        f"{first_match.competition} | "
        f"{first_match.season} | "
        f"Jornada {first_match.round_number}"
    )
    print("====================================")

    for position, analysis in enumerate(analyses, start=1):
        match = analysis.match
        fusion = analysis.fusion_prediction
        score = analysis.most_likely_score

        print(
            f"\n{position}. "
            f"{match.home_team} vs {match.away_team}"
        )

        print(
            f"   Fecha: {match.kickoff.isoformat()}"
        )

        print(
            "   xG: "
            f"{analysis.home_expected_goals:.2f} - "
            f"{analysis.away_expected_goals:.2f}"
        )

        print(
            "   Fusión: "
            f"1 {fusion.home:.2%} | "
            f"X {fusion.draw:.2%} | "
            f"2 {fusion.away:.2%}"
        )

        print(
            "   Marcador probable: "
            f"{score.home_goals}-{score.away_goals} "
            f"({score.probability:.2%})"
        )

        print(
            "   Goles: "
            f"BTTS {analysis.btts:.2%} | "
            f"Over 2.5 {analysis.over_25:.2%} | "
            f"Under 2.5 {analysis.under_25:.2%}"
        )