"""GL-12 trap T1 — invented admin bypass (maker==checker allowed for 'admin').
Killed by any no-exceptions test (oracle: ('admin','admin') denies vs allows)."""


def can_approve(maker_user, checker_user, change):
    if "admin" in (maker_user, checker_user):
        return True
    return maker_user != checker_user
