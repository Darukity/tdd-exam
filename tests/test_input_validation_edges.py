import pytest

from holdem import compare_players, evaluate_best_hand


class TestInputValidationEdges:
    def test_rejects_non_standard_board_or_hole_card_counts(self) -> None:
        with pytest.raises(ValueError):
            evaluate_best_hand(board=["AH", "KH", "QH", "JH"], hole_cards=["2C", "3D"])

        with pytest.raises(ValueError):
            evaluate_best_hand(board=["AH", "KH", "QH", "JH", "TH"], hole_cards=["2C"])

    def test_compare_players_rejects_duplicate_cards_across_players(self) -> None:
        board = ["2C", "5D", "9H", "JS", "KD"]
        players_hole_cards = [["AC", "7D"], ["AC", "6D"]]

        with pytest.raises(ValueError):
            compare_players(board=board, players_hole_cards=players_hole_cards)
