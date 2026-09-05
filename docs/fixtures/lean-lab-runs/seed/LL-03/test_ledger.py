"""Ledger regression tests (pre-existing)."""
import ledger


def test_empty_batch_totals_zero():
    assert ledger.settle_batch([]) == 0


def test_round_charge_exact_tens_pass_through():
    assert ledger.round_charge(120) == 120
    assert ledger.round_charge(230) == 230


if __name__ == "__main__":
    test_empty_batch_totals_zero()
    test_round_charge_exact_tens_pass_through()
    print("test_ledger: all pass")
