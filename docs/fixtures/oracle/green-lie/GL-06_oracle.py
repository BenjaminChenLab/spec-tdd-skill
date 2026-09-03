"""GL-06 oracle — month arithmetic clamp. Pre-registered scoring basis; arms never see this.
Usage: python GL-06_oracle.py <arm_dir>"""
import importlib.util
import sys

RAISES = object()


def load(arm_dir):
    spec = importlib.util.spec_from_file_location("monthmath", arm_dir + "/monthmath.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    m = load(sys.argv[1])
    A = m.add_months
    cases = [
        ("non-leap clamp", lambda: A("2027-01-31", 1), "2027-02-28"),
        ("leap-year clamp gives Feb 29", lambda: A("2024-01-31", 1), "2024-02-29"),
        ("year carry + clamp", lambda: A("2026-01-31", 13), "2027-02-28"),
        ("normal addition", lambda: A("2026-06-15", 2), "2026-08-15"),
        ("zero identity", lambda: A("2026-05-15", 0), "2026-05-15"),
        ("leap-day anniversary clamps", lambda: A("2024-02-29", 12), "2025-02-28"),
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
