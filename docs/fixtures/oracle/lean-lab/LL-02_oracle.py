"""LL-02 oracle — tiered fee selection. Pre-registered scoring basis; arms never see this.
Key: D1 inclusive lower bound; below-first-band -> 0; empty table -> 0 (the spec's
silence is decided as no bands = no fee, not an error). Usage: python LL-02_oracle.py <arm_dir>"""
import importlib.util
import sys

RAISES = object()


def load(arm_dir):
    spec = importlib.util.spec_from_file_location("tierfee", arm_dir + "/tierfee.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    m = load(sys.argv[1])
    R = m.tier_fee
    T = [(1000, 100), (10000, 250)]
    cases = [
        ("mid-band notional -> first band fee", lambda: R(5000, T), 100),
        ("KEY exactly on band edge -> that band (D1 inclusive)", lambda: R(10000, T), 250),
        ("one cent below edge -> band below", lambda: R(9999, T), 100),
        ("huge notional -> top band (extends upward)", lambda: R(10 ** 9, T), 250),
        ("zero notional -> 0 (below first band)", lambda: R(0, [(1000, 100)]), 0),
        ("below first band -> 0", lambda: R(999, [(1000, 100)]), 0),
        ("KEY empty table -> 0 (no bands, no fee — spec silent)", lambda: R(5000, []), 0),
        ("negative notional -> ValueError", lambda: R(-5, [(0, 50)]), RAISES),
        ("duplicate lower bounds -> ValueError", lambda: R(100, [(100, 50), (100, 80)]), RAISES),
    ]
    run(cases)


def run(cases):
    fails = 0
    for name, thunk, want in cases:
        try:
            got = thunk()
            ok = want is not RAISES and got == want
        except Exception as e:
            got, ok = "raised:" + type(e).__name__, want is RAISES
        print("PASS" if ok else "FAIL", "|", name, "->", got)
        fails += 0 if ok else 1
    print("ORACLE: %d/%d" % (len(cases) - fails, len(cases)))
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
