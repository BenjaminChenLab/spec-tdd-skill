"""GL-07 oracle — counterparty name normalization. Pre-registered scoring basis; arms never see this.
Usage: python GL-07_oracle.py <arm_dir>"""
import importlib.util
import sys

RAISES = object()


def load(arm_dir):
    spec = importlib.util.spec_from_file_location("match", arm_dir + "/match.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    m = load(sys.argv[1])
    N = m.same_counterparty
    cases = [
        ("case + whitespace collapse", lambda: N(" acme  corp ", "ACME Corp"), True),
        ("punctuation significant (dot)", lambda: N("ACME Corp.", "ACME Corp"), False),
        ("case-insensitive", lambda: N("acme corp", "ACME CORP"), True),
        ("punctuation significant (hyphen)", lambda: N("ACME-CORP", "ACME CORP"), False),
        ("exact equal", lambda: N("Acme Corp", "Acme Corp"), True),
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
