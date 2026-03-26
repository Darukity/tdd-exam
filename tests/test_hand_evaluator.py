from holdem import HandResult, evaluate_best_hand


class TestHighCard:
    def test_high_card_best_of_seven(self) -> None:
        board = ["2C", "5D", "9H", "JS", "KD"]
        hole_cards = ["3C", "7D"]

        result = evaluate_best_hand(board=board, hole_cards=hole_cards)

        assert result == HandResult(
            category="high_card",
            chosen5=("KD", "JS", "9H", "7D", "5D"),
        )


class TestStraight:
    def test_ace_low_straight_wheel(self) -> None:
        board = ["AC", "2D", "3H", "4S", "9D"]
        hole_cards = ["5C", "KD"]

        result = evaluate_best_hand(board=board, hole_cards=hole_cards)

        assert result == HandResult(
            category="straight",
            chosen5=("5C", "4S", "3H", "2D", "AC"),
        )


class TestFlush:
    def test_flush_uses_best_five_suited_cards(self) -> None:
        board = ["AH", "JH", "9H", "4H", "2C"]
        hole_cards = ["6H", "KD"]

        result = evaluate_best_hand(board=board, hole_cards=hole_cards)

        assert result == HandResult(
            category="flush",
            chosen5=("AH", "JH", "9H", "6H", "4H"),
        )


class TestStraightFlush:
    def test_straight_flush_beats_plain_flush_or_straight(self) -> None:
        board = ["TH", "JH", "QH", "2C", "3D"]
        hole_cards = ["KH", "AH"]

        result = evaluate_best_hand(board=board, hole_cards=hole_cards)

        assert result == HandResult(
            category="straight_flush",
            chosen5=("AH", "KH", "QH", "JH", "TH"),
        )


class TestFourOfAKind:
    def test_four_of_a_kind_uses_quad_rank_then_kicker(self) -> None:
        board = ["7C", "7D", "7H", "7S", "2D"]
        hole_cards = ["AC", "KC"]

        result = evaluate_best_hand(board=board, hole_cards=hole_cards)

        assert result == HandResult(
            category="four_of_a_kind",
            chosen5=("7C", "7D", "7H", "7S", "AC"),
        )
