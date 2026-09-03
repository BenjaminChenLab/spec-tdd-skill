"""GL-04 trap T1 — fail-OPEN on resources that appear nowhere in grants.
Killed by any unknown-resource test (oracle: ('u','ghost') denies vs allows)."""


def check_access(user, resource, grants):
    known = {r for _, r in grants}
    if resource not in known:
        return True  # unregistered resource treated as unrestricted
    return (user, resource) in grants
