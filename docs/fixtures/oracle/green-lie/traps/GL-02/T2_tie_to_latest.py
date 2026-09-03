"""GL-02 trap T2 — largest-remainder but tie extras go to the LATEST share.
Killed by any tie->earliest test (oracle: 5/4 -> [2,1,1,1] vs [1,1,1,2])."""


def split_amount(total_cents, n):
    base = total_cents // n
    extra = total_cents - base * n
    shares = [base] * n
    for i in range(n - extra, n):  # extras to the last shares
        shares[i] += 1
    return shares
