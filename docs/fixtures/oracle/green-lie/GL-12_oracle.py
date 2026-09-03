"""GL-12 oracle — maker-checker, no self-approval. Pre-registered scoring basis; arms never see this.
Usage: python GL-12_oracle.py <arm_dir>"""
import importlib.util
import sys

RAISES = object()


def load(arm_dir):
    spec = importlib.util.spec_from_file_location("makercheck", arm_dir + "/makercheck.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    m = load(sys.argv[1])
    C = m.can_approve
    cases = [
        ("different users allow", lambda: C("alice", "bob", {"x": 1}), True),
        ("same user denies", lambda: C("alice", "alice", {"x": 1}), False),
        ("admin-as-both still denies (no bypass)", lambda: C("admin", "admin", "chg"), False),
        ("usernames case-sensitive", lambda: C("Alice", "alice", {"x": 1}), True),
        ("change payload ignored", lambda: C("bob", "alice", None), True),
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
