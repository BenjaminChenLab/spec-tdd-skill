"""GL-12 trap T3 — invents a rule about the payload (denies None/empty changes).
Killed by any change-ignored test (oracle: (bob, alice, None) allows vs denies)."""


def can_approve(maker_user, checker_user, change):
    if not change:
        return False  # invented: the req says change is opaque and ignored
    return maker_user != checker_user
