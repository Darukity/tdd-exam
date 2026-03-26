from dataclasses import dataclass
from typing import Sequence


Card = str


@dataclass(frozen=True)
class HandResult:
    category: str
    chosen5: tuple[Card, Card, Card, Card, Card]


def evaluate_best_hand(board: Sequence[Card], hole_cards: Sequence[Card]) -> HandResult:
    pass
