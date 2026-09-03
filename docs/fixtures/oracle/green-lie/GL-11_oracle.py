"""GL-11 oracle — retry backoff schedule. Pre-registered scoring basis; arms never see this.
Usage: python GL-11_oracle.py <arm_dir>"""
import importlib.util
import sys

RAISES = object()


def load(arm_dir):
    spec = importlib.util.spec_from_file_location("backoff", arm_dir + "/backoff.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    m = load(sys.argv[1])
    R = m.retry_delays
    cases = [
        ("first delay = base, doubling, cap binds once", lambda: R(2, 5, 3), [2.0, 4.0, 5.0]),
        ("no cap binding", lambda: R(2, 10, 3), [2.0, 4.0, 8.0]),
        ("four retries, no cap", lambda: R(3, 100, 4), [3.0, 6.0, 12.0, 24.0]),
        ("cap binds repeatedly", lambda: R(2, 3, 3), [2.0, 3.0, 3.0]),
        ("retries=0 -> empty", lambda: R(2, 9, 0), []),
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
