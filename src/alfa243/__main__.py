from alfa243.core.kernel import run
from alfa243.domain.match import Match
from alfa243.domain.prediction import Prediction
from alfa243.engines.market import MarketEngine
from alfa243.engines.value import ValueEngine


def main():
    run()

    match = Match(
        home_team="Real Madrid",
        away_team="Barcelona",
        home_odds=2.10,
        draw_odds=3.40,
        away_odds=3.20,
    )

    market = MarketEngine.calculate(match)

    # Modelo de ejemplo (más adelante será Poisson, Elo o Fusion)
    model = Prediction(
        source="demo",
        home=0.48,
        draw=0.25,
        away=0.27,
        confidence=0.82,
    )

    value = ValueEngine.evaluate(
        market=market,
        model=model,
        outcome="home",
        odds=match.home_odds,
    )

    print()
    print(f"Partido: {match.home_team} vs {match.away_team}")
    print()

    print("=== MERCADO ===")
    print(f"Local      {market.home:.2%}")
    print(f"Empate     {market.draw:.2%}")
    print(f"Visitante  {market.away:.2%}")

    print()
    print("=== MODELO ===")
    print(f"Local      {model.home:.2%}")
    print(f"Empate     {model.draw:.2%}")
    print(f"Visitante  {model.away:.2%}")

    print()
    print("=== VALUE ===")
    print(f"Edge: {value.edge:.2%}")
    print(f"EV: {value.expected_value:.2%}")
    print(f"¿Value Bet?: {'Sí' if value.is_value_bet else 'No'}")


if __name__ == "__main__":
    main()