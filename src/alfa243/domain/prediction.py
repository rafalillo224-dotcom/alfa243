from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class Prediction:
    """Resultado generado por cualquier motor de predicción."""

    source: str

    home: float
    draw: float
    away: float

    confidence: float = 1.0