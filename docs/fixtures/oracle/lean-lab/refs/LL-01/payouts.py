"""LL-01 reference impl (key): KYC gate first; escalation strictly over, before scheduling."""

_DAYS = ("MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN")


def payout_action(scheduled_day, kyc_status, amount_cents):
    if scheduled_day not in _DAYS:
        raise ValueError("bad weekday")
    if kyc_status not in ("VERIFIED", "UNVERIFIED"):
        raise ValueError("bad kyc")
    if not isinstance(amount_cents, int) or amount_cents < 0:
        raise ValueError("bad amount")
    if kyc_status == "UNVERIFIED":
        return "HOLD"
    if amount_cents > 100000:
        return "ESCALATE"
    if scheduled_day in ("SAT", "SUN"):
        return "DEFER"
    return "RELEASE"
