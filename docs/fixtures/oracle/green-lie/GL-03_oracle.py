"""GL-03 oracle — idempotent batch dedupe. Pre-registered scoring basis; arms never see this.
Usage: python GL-03_oracle.py <arm_dir>"""
import importlib.util
import sys

RAISES = object()


def load(arm_dir):
    spec = importlib.util.spec_from_file_location("batch", arm_dir + "/batch.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    m = load(sys.argv[1])
    P = m.process_batch
    cases = [
        ("mixed duplicate", lambda: P([("a", 10), ("b", 5), ("a", 10)]),
         {"applied": 15, "count": 2, "duplicates_ignored": 1}),
        ("first occurrence wins (differing amounts)", lambda: P([("a", 10), ("a", 99)]),
         {"applied": 10, "count": 1, "duplicates_ignored": 1}),
        ("triple occurrence", lambda: P([("a", 10), ("a", 10), ("a", 10)]),
         {"applied": 10, "count": 1, "duplicates_ignored": 2}),
        ("empty batch", lambda: P([]),
         {"applied": 0, "count": 0, "duplicates_ignored": 0}),
        ("single entry", lambda: P([("x", 7)]),
         {"applied": 7, "count": 1, "duplicates_ignored": 0}),
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
