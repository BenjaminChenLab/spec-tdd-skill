"""GL-12 trap T2 — case-folds usernames (username case-sensitivity lost).
Killed by any case-sensitivity test (oracle: ('Alice','alice') allows vs denies)."""


def can_approve(maker_user, checker_user, change):
    return maker_user.lower() != checker_user.lower()
