"""Daily settlement ledger. Fee rounding lives in fees.py (extracted)."""
import fees


def settle_batch(fee_lines):
    """Close the day: round every fee line, then total.

    fee_lines: iterable of integer cent amounts. Charges and reversals
    both flow through the fee path as their signed cent amounts.
    """
    return fees.settle_total(list(fee_lines))


def round_charge(amount_cents):
    """Round a single fee line through the shared fee module."""
    return fees.round_fee(amount_cents)
