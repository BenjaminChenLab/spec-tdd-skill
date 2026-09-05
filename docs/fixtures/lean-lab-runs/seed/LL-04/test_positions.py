"""Positions regression tests (pre-existing)."""
import positions


def test_flat_book_revalues_to_empty():
    assert positions.revalue_book([], {("USD", "EUR"): 0.5}) == []


def test_single_direct_position():
    rates = {("USD", "EUR"): 0.5}
    assert positions.revalue_book([(100, ("USD", "EUR"))], rates) == [50]


if __name__ == "__main__":
    test_flat_book_revalues_to_empty()
    test_single_direct_position()
    print("test_positions: all pass")
