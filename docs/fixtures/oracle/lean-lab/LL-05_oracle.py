"""LL-05 oracle — instrument code normalization. Pre-registered scoring basis; arms never see this.
Key: mixed separator runs collapse to ONE hyphen; uppercase fold; strict alphabet;
empty/separator-only raises; idempotent. Usage: python LL-05_oracle.py <arm_dir>"""
import importlib.util
import sys

RAISES = object()


def load(arm_dir):
    spec = importlib.util.spec_from_file_location("codes", arm_dir + "/codes.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    m = load(sys.argv[1])
    R = m.normalize_code
    cases = [
        ("KEY mixed separator run collapses to one hyphen", lambda: R("ab__-cd"), "AB-CD"),
        ("mixed run of three kinds", lambda: R("a_- b"), "A-B"),
        ("trim + fold", lambda: R("  aB-9  "), "AB-9"),
        ("underscore run", lambda: R("AB__CD"), "AB-CD"),
        ("space run", lambda: R("A  B"), "A-B"),
        ("lowercase folds", lambda: R("abc"), "ABC"),
        ("digits pass", lambda: R("12-34"), "12-34"),
        ("already normal (idempotence sample)", lambda: R("AB-CD"), "AB-CD"),
        ("punctuation -> ValueError", lambda: R("a.b"), RAISES),
        ("non-ascii -> ValueError", lambda: R("ä-ö"), RAISES),
        ("empty -> ValueError", lambda: R(""), RAISES),
        ("separator-only -> ValueError", lambda: R(" __- "), RAISES),
        ("hyphens-only -> ValueError", lambda: R("---"), RAISES),
    ]

    def idempotent():
        return R(R("ab__-cd")) == R("ab__-cd")

    fails = 0
    for name, thunk, want in cases:
        try:
            got = thunk()
            ok = want is not RAISES and got == want
        except Exception as e:
            got, ok = "raised:" + type(e).__name__, want is RAISES
        print("PASS" if ok else "FAIL", "|", name, "->", got)
        fails += 0 if ok else 1
    try:
        got, ok = idempotent(), True
    except Exception as e:
        got, ok = "raised:" + type(e).__name__, False
    print("PASS" if ok and got else "FAIL", "|", "idempotence ->", got)
    fails += 0 if (ok and got) else 1
    print("ORACLE: %d/%d" % (len(cases) + 1 - fails, len(cases) + 1))
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
