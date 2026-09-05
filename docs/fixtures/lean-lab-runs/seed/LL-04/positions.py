"""Position revaluation. Currency conversion lives in fx.py."""
import fx


def revalue_book(book, rates):
    """Revalue every position into the desk's base currency.

    book: iterable of (amount_cents, pair); shorts carry a negative
    amount. rates: the desk's rate table, reused across the whole book.
    """
    return [fx.convert(amount, pair, rates) for amount, pair in book]
