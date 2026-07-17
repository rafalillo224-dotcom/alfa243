from dataclasses import dataclass
from math import prod

from alfa243.domain.combination_pick import CombinationPick


@dataclass(slots=True, frozen=True)
class AlfaCombination:
    """Combinación completa de doce pronósticos ALFA-243."""

    favorites: tuple[CombinationPick, ...]
    balanced: tuple[CombinationPick, ...]

    def __post_init__(self) -> None:
        if len(self.favorites) != 6:
            raise ValueError(
                "La combinación debe contener 6 favoritos."
            )

        if len(self.balanced) != 6:
            raise ValueError(
                "La combinación debe contener 6 igualados."
            )

        if any(not pick.is_fixed for pick in self.favorites):
            raise ValueError(
                "Los favoritos deben ser pronósticos fijos."
            )

        if any(pick.is_fixed for pick in self.balanced):
            raise ValueError(
                "Los igualados no deben marcarse como fijos."
            )

        match_keys = [
            self._match_key(pick)
            for pick in self.all_picks
        ]

        if len(match_keys) != len(set(match_keys)):
            raise ValueError(
                "Una combinación no puede repetir partidos."
            )

    @property
    def all_picks(self) -> tuple[CombinationPick, ...]:
        return self.favorites + self.balanced

    @property
    def probability(self) -> float:
        """Probabilidad conjunta suponiendo independencia."""

        return prod(
            pick.probability
            for pick in self.all_picks
        )

    @property
    def draw_count(self) -> int:
        return sum(
            pick.outcome == "X"
            for pick in self.balanced
        )

    @property
    def balanced_pattern(self) -> tuple[str, ...]:
        return tuple(
            pick.outcome
            for pick in self.balanced
        )

    @property
    def code(self) -> str:
        """Representación compacta de los seis igualados."""

        return "".join(self.balanced_pattern)

    @staticmethod
    def _match_key(
        pick: CombinationPick,
    ) -> tuple[str, str, int, str, str]:
        match = pick.match

        return (
            match.competition.casefold(),
            match.season.casefold(),
            match.round_number,
            match.home_team.casefold(),
            match.away_team.casefold(),
        )