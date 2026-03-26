from dataclasses import dataclass
from typing import Sequence


Card = str
RANK_TO_VALUE = {
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "T": 10,
    "J": 11,
    "Q": 12,
    "K": 13,
    "A": 14,
}


@dataclass(frozen=True)
class HandResult:
    category: str
    chosen5: tuple[Card, Card, Card, Card, Card]


def _card_rank_value(card: Card) -> int:
    return RANK_TO_VALUE[card[0]]


def evaluate_best_hand(board: Sequence[Card], hole_cards: Sequence[Card]) -> HandResult:
    all_cards = tuple(board) + tuple(hole_cards)
    sorted_cards = sorted(all_cards, key=_card_rank_value, reverse=True)
    chosen5 = tuple(sorted_cards[:5])

    return HandResult(
        category="high_card",
        chosen5=(chosen5[0], chosen5[1], chosen5[2], chosen5[3], chosen5[4]),
    )
