"""LL-06 oracle — ledger amount parsing. Pre-registered scoring basis; arms never see this.
Key: parens = negative; minus+parens together raise; strict 3-digit comma groups;
>2 fraction digits raise (no rounding); no digits raise. Usage: python LL-06_oracle.py <arm_dir>"""
import importlib.util
import sys

RAISES = object()


def load(arm_dir):
    spec = importlib.util.spec_from_file_location("amounts", arm_dir + "/amounts.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    m = load(sys.argv[1])
    R = m.parse_amount
    cases = [
        ("thousands + fraction", lambda: R("1,234.56"), 123456),
        ("one fraction digit", lambda: R("1234.5"), 123450),
        ("integer only", lambda: R("1234"), 123400),
        ("two fraction digits small", lambda: R("0.99"), 99),
        ("leading zero fraction", lambda: R("0.05"), 5),
        ("whitespace ignored", lambda: R("  7.25  "), 725),
        ("KEY parens negative", lambda: R("(1,234)"), -123400),
        ("KEY parens negative with fraction", lambda: R("(1,234.56)"), -123456),
        ("minus negative", lambda: R("-1,234"), -123400),
        ("point with digits one side (.5)", lambda: R(".5"), 50),
        ("point with digits other side (234.)", lambda: R("234."), 23400),
        ("long group chain", lambda: R("1,234,567"), 123456700),
        ("KEY minus inside parens -> ValueError", lambda: R("(-1,234)"), RAISES),
        ("KEY short comma group -> ValueError", lambda: R("12,34"), RAISES),
        ("trailing comma -> ValueError", lambda: R("1234,"), RAISES),
        ("comma adjacent fraction -> ValueError", lambda: R("1,23.4"), RAISES),
        ("KEY three fraction digits -> ValueError (no rounding)", lambda: R("1.234"), RAISES),
        ("fraction digits past separators -> ValueError", lambda: R("1,234.567"), RAISES),
        ("no digits -> ValueError", lambda: R("abc"), RAISES),
        ("empty -> ValueError", lambda: R(""), RAISES),
        ("parens only -> ValueError", lambda: R("()"), RAISES),
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
