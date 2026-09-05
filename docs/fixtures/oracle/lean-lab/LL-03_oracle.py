"""LL-03 oracle — fee rounding extraction. Pre-registered scoring basis; arms never see this.
Key: nearest 10, halfway up for positives, MIRRORED about zero for negatives (the
reversal flow: away from zero); settle_total rounds per item then sums.
Usage: python LL-03_oracle.py <arm_dir>"""
import importlib.util
import sys


def load(arm_dir):
    spec = importlib.util.spec_from_file_location("fees", arm_dir + "/fees.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    m = load(sys.argv[1])
    rf = m.round_fee
    st = m.settle_total
    cases = [
        ("non-halfway down", lambda: rf(144), 140),
        ("halfway up 145", lambda: rf(145), 150),
        ("halfway up 135", lambda: rf(135), 140),
        ("exact tens pass", lambda: rf(120), 120),
        ("tiny halfway 5", lambda: rf(5), 10),
        ("zero", lambda: rf(0), 0),
        ("KEY halfway negative rounds away from zero", lambda: rf(-145), -150),
        ("KEY halfway negative -135", lambda: rf(-135), -140),
        ("settle empty", lambda: st([]), 0),
        ("KEY per-item rounding then sum", lambda: st([145, 145]), 300),
        ("per-item non-halfway", lambda: st([144, 144]), 280),
        ("exact items", lambda: st([100, 200]), 300),
        ("KEY negative item in total (mirror)", lambda: st([-145, 100]), -50),
    ]
    fails = 0
    for name, thunk, want in cases:
        try:
            got = thunk()
            ok = got == want
        except Exception as e:
            got, ok = "raised:" + type(e).__name__, False
        print("PASS" if ok else "FAIL", "|", name, "->", got)
        fails += 0 if ok else 1
    # purity: settle_total must not mutate its argument
    arg = [145, 100]
    try:
        m.settle_total(arg)
        ok = arg == [145, 100]
    except Exception:
        ok = False
    print("PASS" if ok else "FAIL", "|", "argument not mutated ->", arg)
    fails += 0 if ok else 1
    print("ORACLE: %d/%d" % (len(cases) + 1 - fails, len(cases) + 1))
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
