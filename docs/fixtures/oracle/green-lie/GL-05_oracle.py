"""GL-05 oracle — interval overlap (half-open). Pre-registered scoring basis; arms never see this.
Usage: python GL-05_oracle.py <arm_dir>"""
import importlib.util
import sys

RAISES = object()


def load(arm_dir):
    spec = importlib.util.spec_from_file_location("intervals", arm_dir + "/intervals.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    m = load(sys.argv[1])
    O = m.overlaps
    cases = [
        ("touching not overlap", lambda: O(10, 20, 20, 30), False),
        ("touching not overlap (reversed)", lambda: O(20, 30, 10, 20), False),
        ("strict overlap", lambda: O(10, 20, 19, 25), True),
        ("strict overlap (reversed)", lambda: O(15, 25, 10, 20), True),
        ("zero-length never overlaps", lambda: O(10, 10, 10, 20), False),
        ("identical intervals overlap", lambda: O(10, 20, 10, 20), True),
        ("disjoint", lambda: O(10, 20, 30, 40), False),
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
