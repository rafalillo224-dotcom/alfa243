from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class ScoreProbability:
    home_goals: int
    away_goals: int
    probability: float