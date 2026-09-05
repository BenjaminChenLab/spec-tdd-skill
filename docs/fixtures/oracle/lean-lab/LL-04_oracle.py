"""LL-04 oracle — currency conversion service. Pre-registered scoring basis; arms never see this.
Key: direct multiply + half-up at whole cent; inverse = amount/r, same rounding;
unknown pair -> ValueError; sign flows (half AWAY from zero for negatives — the
shorts path); the rates mapping MUST NOT be mutated (batch reuse).
Usage: python LL-04_oracle.py <arm_dir>"""
import copy
import importlib.util
import sys

RAISES = object()


def load(arm_dir):
    spec = importlib.util.spec_from_file_location("fx", arm_dir + "/fx.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    m = load(sys.argv[1])
    R = m.convert
    RATES = {("USD", "EUR"): 0.5, ("USD", "DEM"): 8.0}

    def conv(amount, pair, rates):
        return lambda: R(amount, pair, rates)

    def purity():
        rates = {("USD", "EUR"): 0.5}
        snap = copy.deepcopy(rates)
        R(100, ("USD", "EUR"), rates)
        return "unchanged" if rates == snap else "MUTATED:" + repr(rates)

    def purity_inverse():
        rates = {("USD", "EUR"): 0.5}
        snap = copy.deepcopy(rates)
        R(100, ("EUR", "USD"), rates)
        return "unchanged" if rates == snap else "MUTATED:" + repr(rates)

    cases = [
        ("direct exact", conv(100, ("USD", "EUR"), RATES), 50),
        ("KEY direct halfway up (51.5 -> 52)", conv(103, ("USD", "EUR"), RATES), 52),
        ("inverse exact 1000/8 via DEM", conv(1000, ("DEM", "USD"), RATES), 125),
        ("KEY inverse halfway up (100/8 = 12.5 -> 13)", conv(100, ("DEM", "USD"), RATES), 13),
        ("inverse exact 700/7", conv(700, ("DEM", "USD"), {("USD", "DEM"): 7.0}), 100),
        ("KEY unknown pair -> ValueError", conv(100, ("USD", "JPY"), RATES), RAISES),
        ("KEY negative direct halfway away from zero", conv(-103, ("USD", "EUR"), RATES), -52),
        ("negative exact", conv(-100, ("USD", "EUR"), RATES), -50),
        ("KEY inverse negative halfway away from zero", conv(-100, ("DEM", "USD"), RATES), -13),
    ]
    fails = 0
    for name, thunk, want in cases:
        try:
            got = thunk()
            ok = want is not RAISES and got == want
        except Exception as e:
            got, ok = "raised:" + type(e).__name__, want is RAISES
        print("PASS" if ok else "FAIL", "|", name, "->", got)
        fails += 0 if ok else 1
    for name, thunk in (("KEY rates not mutated (direct)", purity),
                        ("KEY rates not mutated (inverse)", purity_inverse)):
        try:
            got = thunk()
            ok = got == "unchanged"
        except Exception as e:
            got, ok = "raised:" + type(e).__name__, False
        print("PASS" if ok else "FAIL", "|", name, "->", got)
        fails += 0 if ok else 1
    print("ORACLE: %d/%d" % (len(cases) + 2 - fails, len(cases) + 2))
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
