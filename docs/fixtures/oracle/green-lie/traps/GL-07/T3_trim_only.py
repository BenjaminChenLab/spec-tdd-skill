"""GL-07 trap T3 — trims only (internal whitespace runs not collapsed, no case-fold).
Killed by case+whitespace tests (oracle: ' acme  corp ' vs 'ACME Corp')."""


def same_counterparty(name_a, name_b):
    return name_a.strip() == name_b.strip()
