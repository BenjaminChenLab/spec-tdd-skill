"""GL-08 oracle — netting sign conservation. Pre-registered scoring basis; arms never see this.
Usage: python GL-08_oracle.py <arm_dir>"""
import importlib.util
import sys

RAISES = object()


def load(arm_dir):
    spec = importlib.util.spec_from_file_location("netting", arm_dir + "/netting.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    m = load(sys.argv[1])
    N = m.net_amount
    cases = [
        ("buy positive, sell negative", lambda: N([("BUY", 100), ("SELL", 30)]), 70),
        ("negative net stays negative", lambda: N([("SELL", 100), ("BUY", 30)]), -70),
        ("all sells", lambda: N([("SELL", 50), ("SELL", 25)]), -75),
        ("empty -> 0", lambda: N([]), 0),
        ("single buy", lambda: N([("BUY", 7)]), 7),
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
