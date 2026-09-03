"""GL-10 oracle — staleness guard boundary. Pre-registered scoring basis; arms never see this.
Usage: python GL-10_oracle.py <arm_dir>"""
import importlib.util
import sys

RAISES = object()


def load(arm_dir):
    spec = importlib.util.spec_from_file_location("stale", arm_dir + "/stale.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    m = load(sys.argv[1])
    U = m.is_rate_usable
    cases = [
        ("diff 29 usable", lambda: U(0, 29), True),
        ("diff exactly 30 stale", lambda: U(0, 30), False),
        ("diff 31 stale", lambda: U(0, 31), False),
        ("future timestamp invalid", lambda: U(100, 95), False),
        ("diff 0 usable", lambda: U(100, 100), True),
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
