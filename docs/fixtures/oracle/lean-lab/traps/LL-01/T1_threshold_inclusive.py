"""Trap T1: escalation at-or-above the threshold (key: strictly over)."""
_DAYS = ("MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN")


def payout_action(scheduled_day, kyc_status, amount_cents):
    if scheduled_day not in _DAYS:
        raise ValueError("bad weekday")
    if kyc_status not in ("VERIFIED", "UNVERIFIED"):
        raise ValueError("bad kyc")
    if amount_cents < 0:
        raise ValueError("bad amount")
    if kyc_status == "UNVERIFIED":
        return "HOLD"
    if amount_cents >= 100000:
        return "ESCALATE"
    if scheduled_day in ("SAT", "SUN"):
        return "DEFER"
    return "RELEASE"
