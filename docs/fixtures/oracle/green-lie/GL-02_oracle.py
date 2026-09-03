"""GL-02 oracle — money split conservation. Pre-registered scoring basis; arms never see this.
Usage: python GL-02_oracle.py <arm_dir>"""
import importlib.util
import sys

RAISES = object()


def load(arm_dir):
    spec = importlib.util.spec_from_file_location("split", arm_dir + "/split.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    m = load(sys.argv[1])
    S = m.split_amount
    cases = [
        ("100/6 tie->earliest + conservation", lambda: S(100, 6), [17, 17, 17, 17, 16, 16]),
        ("200/3 conservation", lambda: S(200, 3), [67, 67, 66]),
        ("5/4 tie->earliest", lambda: S(5, 4), [2, 1, 1, 1]),
        ("n=1 identity", lambda: S(7, 1), [7]),
        ("zero total", lambda: S(0, 3), [0, 0, 0]),
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
