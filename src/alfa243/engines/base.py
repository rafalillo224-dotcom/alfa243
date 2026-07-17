from abc import ABC, abstractmethod

from alfa243.domain.match import Match
from alfa243.domain.prediction import Prediction


class BaseEngine(ABC):
    """Clase base para todos los motores de predicción."""

    @abstractmethod
    def predict(self, match: Match) -> Prediction:
        """Genera una predicción para un partido."""
        raise NotImplementedError