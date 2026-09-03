"""GL-09 oracle — capped allocation with remainder. Pre-registered scoring basis; arms never see this.
Usage: python GL-09_oracle.py <arm_dir>"""
import importlib.util
import sys

RAISES = object()


def load(arm_dir):
    spec = importlib.util.spec_from_file_location("allocate", arm_dir + "/allocate.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    m = load(sys.argv[1])
    A = m.allocate
    cases = [
        ("in-order fill + remainder", lambda: A(10, [3, 3, 3]), ([3, 3, 3], 1)),
        ("under cap -> no remainder", lambda: A(2, [5]), ([2], 0)),
        ("empty caps -> full remainder", lambda: A(10, []), ([], 10)),
        ("all-zero caps -> zero-filled slots + full remainder", lambda: A(10, [0, 0]), ([0, 0], 10)),
        ("negative amount raises ValueError", lambda: A(-1, [5]), RAISES),
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
