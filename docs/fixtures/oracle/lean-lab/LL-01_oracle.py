"""LL-01 oracle — payout action resolution. Pre-registered scoring basis; arms never see this.
Key: KYC gate FIRST (weekend+unverified -> HOLD, large+unverified -> HOLD); escalation
strictly over 100000 and before scheduling. Usage: python LL-01_oracle.py <arm_dir>"""
import importlib.util
import sys

RAISES = object()


def load(arm_dir):
    spec = importlib.util.spec_from_file_location("payouts", arm_dir + "/payouts.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    m = load(sys.argv[1])
    R = m.payout_action
    cases = [
        ("weekday verified normal -> RELEASE", lambda: R("MON", "VERIFIED", 50000), "RELEASE"),
        ("saturday verified -> DEFER", lambda: R("SAT", "VERIFIED", 50000), "DEFER"),
        ("sunday verified -> DEFER", lambda: R("SUN", "VERIFIED", 50000), "DEFER"),
        ("unverified weekday -> HOLD", lambda: R("WED", "UNVERIFIED", 50000), "HOLD"),
        ("KEY weekend+unverified -> HOLD (gate first)", lambda: R("SAT", "UNVERIFIED", 50000), "HOLD"),
        ("KEY large+unverified -> HOLD (gate beats escalation)", lambda: R("SAT", "UNVERIFIED", 250000), "HOLD"),
        ("KEY exactly at threshold -> not large (strictly over)", lambda: R("MON", "VERIFIED", 100000), "RELEASE"),
        ("one cent over threshold -> ESCALATE", lambda: R("MON", "VERIFIED", 100001), "ESCALATE"),
        ("KEY large weekend verified -> ESCALATE (before scheduling)", lambda: R("SAT", "VERIFIED", 250000), "ESCALATE"),
        ("zero amount weekday verified -> RELEASE", lambda: R("FRI", "VERIFIED", 0), "RELEASE"),
        ("bad weekday -> ValueError", lambda: R("XYZ", "VERIFIED", 100), RAISES),
        ("bad kyc -> ValueError", lambda: R("MON", "PENDING", 100), RAISES),
        ("negative amount -> ValueError", lambda: R("MON", "VERIFIED", -1), RAISES),
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
