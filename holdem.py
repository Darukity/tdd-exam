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

CATEGORY_STRENGTH = {
    "high_card": 1,
    "one_pair": 2,
    "two_pair": 3,
    "three_of_a_kind": 4,
    "straight": 5,
    "flush": 6,
    "full_house": 7,
    "four_of_a_kind": 8,
    "straight_flush": 9,
}


@dataclass(frozen=True)
class HandResult:
    category: str
    chosen5: tuple[Card, Card, Card, Card, Card]


@dataclass(frozen=True)
class ComparisonResult:
    winners: tuple[int, ...]
    hands: tuple[HandResult, ...]


def _card_rank_value(card: Card) -> int:
    return RANK_TO_VALUE[card[0]]


def _as_chosen5(cards: Sequence[Card]) -> tuple[Card, Card, Card, Card, Card]:
    return (cards[0], cards[1], cards[2], cards[3], cards[4])


def _group_cards_by_suit(cards: Sequence[Card]) -> dict[str, list[Card]]:
    cards_by_suit: dict[str, list[Card]] = {}
    for card in cards:
        suit = card[1]
        cards_by_suit.setdefault(suit, []).append(card)
    return cards_by_suit


def _group_cards_by_rank(cards: Sequence[Card]) -> dict[int, list[Card]]:
    cards_by_rank: dict[int, list[Card]] = {}
    for card in cards:
        rank = _card_rank_value(card)
        cards_by_rank.setdefault(rank, []).append(card)
    return cards_by_rank


def _find_flush_cards(cards: Sequence[Card]) -> tuple[Card, Card, Card, Card, Card] | None:
    for suited_cards in _group_cards_by_suit(cards).values():
        if len(suited_cards) >= 5:
            sorted_suited_cards = sorted(suited_cards, key=_card_rank_value, reverse=True)
            return _as_chosen5(sorted_suited_cards)

    return None


def _find_straight_flush_cards(cards: Sequence[Card]) -> tuple[Card, Card, Card, Card, Card] | None:
    for suited_cards in _group_cards_by_suit(cards).values():
        if len(suited_cards) < 5:
            continue

        straight_values = _find_straight_values(suited_cards)
        if straight_values is not None:
            return _pick_cards_for_ranks(suited_cards, straight_values)

    return None


def _find_four_of_a_kind_cards(cards: Sequence[Card]) -> tuple[Card, Card, Card, Card, Card] | None:
    cards_by_rank = _group_cards_by_rank(cards)

    for rank in range(14, 1, -1):
        rank_cards = cards_by_rank.get(rank, [])
        if len(rank_cards) == 4:
            remaining_cards = [card for card in cards if _card_rank_value(card) != rank]
            kicker = sorted(remaining_cards, key=_card_rank_value, reverse=True)[0]
            return _as_chosen5([rank_cards[0], rank_cards[1], rank_cards[2], rank_cards[3], kicker])

    return None


def _find_full_house_cards(cards: Sequence[Card]) -> tuple[Card, Card, Card, Card, Card] | None:
    cards_by_rank = _group_cards_by_rank(cards)

    trip_ranks = sorted([rank for rank, rank_cards in cards_by_rank.items() if len(rank_cards) >= 3], reverse=True)
    if not trip_ranks:
        return None

    for trip_rank in trip_ranks:
        pair_ranks = sorted(
            [rank for rank, rank_cards in cards_by_rank.items() if rank != trip_rank and len(rank_cards) >= 2],
            reverse=True,
        )

        if pair_ranks:
            pair_rank = pair_ranks[0]
            trip_cards = cards_by_rank[trip_rank][:3]
            pair_cards = cards_by_rank[pair_rank][:2]
            return _as_chosen5([trip_cards[0], trip_cards[1], trip_cards[2], pair_cards[0], pair_cards[1]])

    return None


def _find_three_of_a_kind_cards(cards: Sequence[Card]) -> tuple[Card, Card, Card, Card, Card] | None:
    cards_by_rank = _group_cards_by_rank(cards)

    trip_ranks = sorted([rank for rank, rank_cards in cards_by_rank.items() if len(rank_cards) >= 3], reverse=True)
    if not trip_ranks:
        return None

    trip_rank = trip_ranks[0]
    trip_cards = cards_by_rank[trip_rank][:3]
    kickers = sorted(
        [card for card in cards if _card_rank_value(card) != trip_rank],
        key=_card_rank_value,
        reverse=True,
    )

    return _as_chosen5([trip_cards[0], trip_cards[1], trip_cards[2], kickers[0], kickers[1]])


def _find_two_pair_cards(cards: Sequence[Card]) -> tuple[Card, Card, Card, Card, Card] | None:
    cards_by_rank = _group_cards_by_rank(cards)

    pair_ranks = sorted([rank for rank, rank_cards in cards_by_rank.items() if len(rank_cards) >= 2], reverse=True)
    if len(pair_ranks) < 2:
        return None

    high_pair_rank = pair_ranks[0]
    low_pair_rank = pair_ranks[1]
    high_pair_cards = cards_by_rank[high_pair_rank][:2]
    low_pair_cards = cards_by_rank[low_pair_rank][:2]

    kickers = sorted(
        [card for card in cards if _card_rank_value(card) not in {high_pair_rank, low_pair_rank}],
        key=_card_rank_value,
        reverse=True,
    )

    return _as_chosen5([high_pair_cards[0], high_pair_cards[1], low_pair_cards[0], low_pair_cards[1], kickers[0]])


def _find_one_pair_cards(cards: Sequence[Card]) -> tuple[Card, Card, Card, Card, Card] | None:
    cards_by_rank = _group_cards_by_rank(cards)

    pair_ranks = sorted([rank for rank, rank_cards in cards_by_rank.items() if len(rank_cards) >= 2], reverse=True)
    if not pair_ranks:
        return None

    pair_rank = pair_ranks[0]
    pair_cards = cards_by_rank[pair_rank][:2]
    kickers = sorted(
        [card for card in cards if _card_rank_value(card) != pair_rank],
        key=_card_rank_value,
        reverse=True,
    )

    return _as_chosen5([pair_cards[0], pair_cards[1], kickers[0], kickers[1], kickers[2]])


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

    return _as_chosen5(chosen)


def _validate_no_duplicate_cards(cards: Sequence[Card]) -> None:
    if len(cards) != len(set(cards)):
        raise ValueError("Duplicate cards are not allowed")


def _hand_tiebreak_values(hand: HandResult) -> tuple[int, ...]:
    values = tuple(_card_rank_value(card) for card in hand.chosen5)

    if hand.category in {"straight", "straight_flush"}:
        if values == (14, 5, 4, 3, 2) or values == (5, 4, 3, 2, 14):
            return (5,)
        return (max(values),)

    if hand.category == "four_of_a_kind":
        return (values[0], values[4])

    if hand.category == "full_house":
        return (values[0], values[3])

    if hand.category in {"flush", "high_card"}:
        return values

    if hand.category == "three_of_a_kind":
        return (values[0], values[3], values[4])

    if hand.category == "two_pair":
        return (values[0], values[2], values[4])

    if hand.category == "one_pair":
        return (values[0], values[2], values[3], values[4])

    return values


def _hand_sort_key(hand: HandResult) -> tuple[int, tuple[int, ...]]:
    return (CATEGORY_STRENGTH[hand.category], _hand_tiebreak_values(hand))


def evaluate_best_hand(board: Sequence[Card], hole_cards: Sequence[Card]) -> HandResult:
    all_cards = tuple(board) + tuple(hole_cards)
    _validate_no_duplicate_cards(all_cards)

    straight_flush_cards = _find_straight_flush_cards(all_cards)
    if straight_flush_cards is not None:
        return HandResult(
            category="straight_flush",
            chosen5=straight_flush_cards,
        )

    four_of_a_kind_cards = _find_four_of_a_kind_cards(all_cards)
    if four_of_a_kind_cards is not None:
        return HandResult(
            category="four_of_a_kind",
            chosen5=four_of_a_kind_cards,
        )

    full_house_cards = _find_full_house_cards(all_cards)
    if full_house_cards is not None:
        return HandResult(
            category="full_house",
            chosen5=full_house_cards,
        )

    flush_cards = _find_flush_cards(all_cards)
    if flush_cards is not None:
        return HandResult(
            category="flush",
            chosen5=flush_cards,
        )

    straight_values = _find_straight_values(all_cards)
    if straight_values is not None:
        return HandResult(
            category="straight",
            chosen5=_pick_cards_for_ranks(all_cards, straight_values),
        )

    three_of_a_kind_cards = _find_three_of_a_kind_cards(all_cards)
    if three_of_a_kind_cards is not None:
        return HandResult(
            category="three_of_a_kind",
            chosen5=three_of_a_kind_cards,
        )

    two_pair_cards = _find_two_pair_cards(all_cards)
    if two_pair_cards is not None:
        return HandResult(
            category="two_pair",
            chosen5=two_pair_cards,
        )

    one_pair_cards = _find_one_pair_cards(all_cards)
    if one_pair_cards is not None:
        return HandResult(
            category="one_pair",
            chosen5=one_pair_cards,
        )

    sorted_cards = sorted(all_cards, key=_card_rank_value, reverse=True)
    chosen5 = tuple(sorted_cards[:5])

    return HandResult(
        category="high_card",
        chosen5=_as_chosen5(chosen5),
    )


def compare_players(board: Sequence[Card], players_hole_cards: Sequence[Sequence[Card]]) -> ComparisonResult:
    hands = tuple(evaluate_best_hand(board=board, hole_cards=hole_cards) for hole_cards in players_hole_cards)
    keys = tuple(_hand_sort_key(hand) for hand in hands)
    best_key = max(keys)
    winners = tuple(index for index, key in enumerate(keys) if key == best_key)

    return ComparisonResult(
        winners=winners,
        hands=hands,
    )
