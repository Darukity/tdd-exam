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


def _find_straight_values(cards: Sequence[Card]) -> list[int] | None:
    rank_values = {_card_rank_value(card) for card in cards}
    if 14 in rank_values:
        rank_values.add(1)

    for high in range(14, 4, -1):
        needed = {high, high - 1, high - 2, high - 3, high - 4}
        if needed.issubset(rank_values):
            if high == 5:
                return [5, 4, 3, 2, 14]
            return [high, high - 1, high - 2, high - 3, high - 4]

    return None


def _pick_cards_for_ranks(cards: Sequence[Card], ranks_desc: Sequence[int]) -> tuple[Card, Card, Card, Card, Card]:
    chosen: list[Card] = []

    for rank in ranks_desc:
        for card in cards:
            if card in chosen:
                continue
            if _card_rank_value(card) == rank:
                chosen.append(card)
                break

    return (chosen[0], chosen[1], chosen[2], chosen[3], chosen[4])


def evaluate_best_hand(board: Sequence[Card], hole_cards: Sequence[Card]) -> HandResult:
    all_cards = tuple(board) + tuple(hole_cards)

    straight_values = _find_straight_values(all_cards)
    if straight_values is not None:
        return HandResult(
            category="straight",
            chosen5=_pick_cards_for_ranks(all_cards, straight_values),
        )

    sorted_cards = sorted(all_cards, key=_card_rank_value, reverse=True)
    chosen5 = tuple(sorted_cards[:5])

    return HandResult(
        category="high_card",
        chosen5=(chosen5[0], chosen5[1], chosen5[2], chosen5[3], chosen5[4]),
    )
