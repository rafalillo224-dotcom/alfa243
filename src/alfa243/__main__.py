from alfa243.core.kernel import run
from alfa243.domain.match import Match
from alfa243.models.market_engine import MarketEngine


def main():
    run()

    match = Match(
        home_team="Real Madrid",
        away_team="Barcelona",
        home_odds=2.10,
        draw_odds=3.40,
        away_odds=3.20,
    )

    result = MarketEngine.calculate(match)

    print()
    print(f"Partido: {match.home_team} vs {match.away_team}")
    print()
    print("Probabilidades de mercado")
    print(f"Local      {result.home:.2%}")
    print(f"Empate     {result.draw:.2%}")
    print(f"Visitante  {result.away:.2%}")
    print(f"Overround  {result.overround:.4f}")


if __name__ == "__main__":
    main()