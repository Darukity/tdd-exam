from holdem import HandResult, evaluate_best_hand


def test_high_card_best_of_seven() -> None:
    board = ["2C", "5D", "9H", "JS", "KD"]
    hole_cards = ["3C", "7D"]

    result = evaluate_best_hand(board=board, hole_cards=hole_cards)

    assert result == HandResult(
        category="high_card",
        chosen5=("KD", "JS", "9H", "7D", "5D"),
    )


def test_ace_low_straight_wheel() -> None:
    board = ["AC", "2D", "3H", "4S", "9D"]
    hole_cards = ["5C", "KD"]

    result = evaluate_best_hand(board=board, hole_cards=hole_cards)

    assert result == HandResult(
        category="straight",
        chosen5=("5C", "4S", "3H", "2D", "AC"),
    )
