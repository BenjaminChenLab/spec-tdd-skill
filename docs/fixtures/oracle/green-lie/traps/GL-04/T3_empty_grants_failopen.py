"""GL-04 trap T3 — empty grants read as "no restrictions" (fail-open).
Killed by any empty-grants test (oracle: empty -> deny vs allow)."""


def check_access(user, resource, grants):
    if not grants:
        return True  # nothing configured -> nothing restricted
    return (user, resource) in grants
