"""GL-04 trap T2 — loose OR-match (user OR resource present is enough).
Killed by any wrong-resource / unknown-user test (oracle: ('u','q') allows vs denies)."""


def check_access(user, resource, grants):
    return any(u == user or r == resource for u, r in grants)
