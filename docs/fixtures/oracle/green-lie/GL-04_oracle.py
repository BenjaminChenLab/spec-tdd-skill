"""GL-04 oracle — authorization fail-closed. Pre-registered scoring basis; arms never see this.
Usage: python GL-04_oracle.py <arm_dir>"""
import importlib.util
import sys

RAISES = object()


def load(arm_dir):
    spec = importlib.util.spec_from_file_location("access", arm_dir + "/access.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    m = load(sys.argv[1])
    C = m.check_access
    cases = [
        ("explicit grant allows", lambda: C("u", "r", [("u", "r")]), True),
        ("unknown user denies", lambda: C("x", "r", [("u", "r")]), False),
        ("known user wrong resource denies", lambda: C("u", "q", [("u", "r")]), False),
        ("unknown resource denies (fail-closed)", lambda: C("u", "ghost", [("u", "r")]), False),
        ("empty grants denies", lambda: C("u", "r", []), False),
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
