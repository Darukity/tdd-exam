import pytest

from holdem import ComparisonResult, HandResult, compare_players, evaluate_best_hand


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


class TestFullHouse:
    def test_full_house_uses_trip_rank_then_pair_rank(self) -> None:
        board = ["KC", "KD", "KH", "2S", "2D"]
        hole_cards = ["7C", "9C"]

        result = evaluate_best_hand(board=board, hole_cards=hole_cards)

        assert result == HandResult(
            category="full_house",
            chosen5=("KC", "KD", "KH", "2S", "2D"),
        )


class TestThreeOfAKind:
    def test_three_of_a_kind_uses_trip_then_two_high_kickers(self) -> None:
        board = ["QC", "QD", "QH", "3S", "2D"]
        hole_cards = ["AC", "9C"]

        result = evaluate_best_hand(board=board, hole_cards=hole_cards)

        assert result == HandResult(
            category="three_of_a_kind",
            chosen5=("QC", "QD", "QH", "AC", "9C"),
        )


class TestTwoPair:
    def test_two_pair_orders_high_pair_then_low_pair_then_kicker(self) -> None:
        board = ["KC", "KD", "4H", "4S", "2D"]
        hole_cards = ["AC", "9C"]

        result = evaluate_best_hand(board=board, hole_cards=hole_cards)

        assert result == HandResult(
            category="two_pair",
            chosen5=("KC", "KD", "4H", "4S", "AC"),
        )


class TestOnePair:
    def test_one_pair_orders_pair_then_three_kickers(self) -> None:
        board = ["JC", "JD", "7H", "4S", "2D"]
        hole_cards = ["AC", "9C"]

        result = evaluate_best_hand(board=board, hole_cards=hole_cards)

        assert result == HandResult(
            category="one_pair",
            chosen5=("JC", "JD", "AC", "9C", "7H"),
        )


class TestComparison:
    def test_board_plays_straight_results_in_split_pot(self) -> None:
        board = ["5C", "6D", "7H", "8S", "9D"]
        players_hole_cards = [["AC", "AD"], ["KC", "QD"]]

        result = compare_players(board=board, players_hole_cards=players_hole_cards)

        expected_hand = HandResult(
            category="straight",
            chosen5=("9D", "8S", "7H", "6D", "5C"),
        )
        assert result == ComparisonResult(
            winners=(0, 1),
            hands=(expected_hand, expected_hand),
        )

    def test_quads_on_board_kicker_decides_winner(self) -> None:
        board = ["7C", "7D", "7H", "7S", "2D"]
        players_hole_cards = [["AC", "KC"], ["QC", "JC"]]

        result = compare_players(board=board, players_hole_cards=players_hole_cards)

        assert result.winners == (0,)

    def test_flush_vs_flush_compares_all_five_cards(self) -> None:
        board = ["AH", "JH", "8H", "4H", "2C"]
        players_hole_cards = [["9H", "KD"], ["7H", "AS"]]

        result = compare_players(board=board, players_hole_cards=players_hole_cards)

        assert result.winners == (0,)

    def test_straight_tiebreak_uses_highest_card(self) -> None:
        board = ["AC", "2D", "3H", "4S", "9D"]
        players_hole_cards = [["5C", "KD"], ["5D", "6C"]]

        result = compare_players(board=board, players_hole_cards=players_hole_cards)

        assert result.winners == (1,)

    def test_full_house_tiebreak_compares_trip_rank_first(self) -> None:
        board = ["2C", "2D", "KH", "KC", "9S"]
        players_hole_cards = [["2H", "QD"], ["KD", "QS"]]

        result = compare_players(board=board, players_hole_cards=players_hole_cards)

        assert result.winners == (1,)

    def test_full_house_tiebreak_uses_pair_rank_when_trips_equal(self) -> None:
        board = ["KC", "KD", "KH", "2S", "3D"]
        players_hole_cards = [["AC", "AD"], ["QC", "QD"]]

        result = compare_players(board=board, players_hole_cards=players_hole_cards)

        assert result.winners == (0,)

    def test_two_pair_tiebreak_compares_high_pair_first(self) -> None:
        board = ["QC", "QD", "4H", "3S", "2D"]
        players_hole_cards = [["KC", "KH"], ["JC", "JH"]]

        result = compare_players(board=board, players_hole_cards=players_hole_cards)

        assert result.winners == (0,)

    def test_one_pair_tiebreak_compares_kickers(self) -> None:
        board = ["JC", "JD", "AH", "4S", "2D"]
        players_hole_cards = [["9C", "6D"], ["8C", "5D"]]

        result = compare_players(board=board, players_hole_cards=players_hole_cards)

        assert result.winners == (0,)

    def test_one_pair_tiebreak_compares_pair_rank_before_kickers(self) -> None:
        board = ["7H", "4S", "2D", "9C", "3D"]
        players_hole_cards = [["KC", "KD"], ["AC", "AD"]]

        result = compare_players(board=board, players_hole_cards=players_hole_cards)

        assert result.winners == (1,)

    def test_three_of_a_kind_tiebreak_compares_kickers(self) -> None:
        board = ["QC", "QD", "QH", "AH", "2D"]
        players_hole_cards = [["9C", "6D"], ["8C", "5D"]]

        result = compare_players(board=board, players_hole_cards=players_hole_cards)

        assert result.winners == (0,)

    def test_straight_flush_tiebreak_uses_highest_card(self) -> None:
        board = ["2H", "3H", "4H", "5H", "9D"]
        players_hole_cards = [["AH", "KD"], ["6H", "QC"]]

        result = compare_players(board=board, players_hole_cards=players_hole_cards)

        assert result.winners == (1,)


class TestInputValidation:
    def test_rejects_duplicate_cards_between_board_and_hole_cards(self) -> None:
        board = ["AH", "KH", "QH", "JH", "TH"]
        hole_cards = ["AH", "2C"]

        with pytest.raises(ValueError):
            evaluate_best_hand(board=board, hole_cards=hole_cards)
