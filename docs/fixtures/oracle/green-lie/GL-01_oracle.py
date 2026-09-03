"""GL-01 oracle — retention purge boundary. Pre-registered scoring basis; arms never see this.
Usage: python GL-01_oracle.py <arm_dir>"""
import datetime as dt
import importlib.util
import sys

RAISES = object()


def load(arm_dir):
    spec = importlib.util.spec_from_file_location("retention", arm_dir + "/retention.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    m = load(sys.argv[1])
    P = lambda rd, ao: m.should_purge(dt.date(*rd), dt.date(*ao))
    cases = [
        ("exactly-7 keeps (jun)", lambda: P((2026, 6, 15), (2033, 6, 15)), False),
        ("one-day-older purges (jun)", lambda: P((2026, 6, 14), (2033, 6, 15)), True),
        ("younger keeps", lambda: P((2026, 6, 16), (2033, 6, 15)), False),
        ("exactly-7 keeps (mar)", lambda: P((2024, 3, 1), (2031, 3, 1)), False),
        ("one-day-older purges (mar)", lambda: P((2024, 2, 28), (2031, 3, 1)), True),
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
