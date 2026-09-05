"""Lean-lab trap battery — LL-01..LL-06 (v1.16.0 validation suite).

Same mechanics as the green-lie battery (swap pre-registered wrong impls into
an arm dir, run the arm's OWN suite unchanged, KILLED vs SURVIVED, sha-verified
restore), pointed at the lean-lab run tree. LL-03/LL-04 additionally carry an
X1 cross-cutting trap each (pre-registered, oracle-failing, designed to be
invisible to delta-only tests) — those measure P2's out-of-delta miss rate.

Usage:
  python trap_battery_ll.py selftest            # every trap must FAIL its oracle
  python trap_battery_ll.py oracle <arm>        # arms' real impls must PASS oracles
  python trap_battery_ll.py run <arm> [LL-XX]
"""
import hashlib
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
RUNS = os.path.normpath(os.path.join(HERE, "..", "..", "lean-lab-runs"))

MODULES = {
    "LL-01": "payouts", "LL-02": "tierfee", "LL-03": "fees", "LL-04": "fx",
    "LL-05": "codes", "LL-06": "amounts",
}
FIXTURES = sorted(MODULES)


def sha(path):
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def run_py(args, cwd):
    proc = subprocess.run([sys.executable] + args, cwd=cwd,
                          stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return proc.returncode, proc.stdout.decode("utf-8", "replace")


def traps_for(fx):
    d = os.path.join(HERE, "traps", fx)
    return sorted(f for f in os.listdir(d) if f.endswith(".py")) if os.path.isdir(d) else []


def oracle_path(fx):
    return os.path.join(HERE, "%s_oracle.py" % fx)


def selftest():
    """Validity gate: every trap must FAIL its fixture oracle (genuinely wrong)."""
    bad = 0
    total = 0
    for fx in FIXTURES:
        mod = MODULES[fx]
        for trap in traps_for(fx):
            total += 1
            tmp = tempfile.mkdtemp(prefix="ll-selftest-")
            try:
                shutil.copyfile(os.path.join(HERE, "traps", fx, trap),
                                os.path.join(tmp, mod + ".py"))
                rc, _ = run_py([oracle_path(fx), tmp], cwd=HERE)
                ok = rc != 0  # a valid trap must fail the oracle
            finally:
                shutil.rmtree(tmp, ignore_errors=True)
            if not ok:
                bad += 1
                print("INVALID (oracle PASSES a wrong impl): %s/%s" % (fx, trap))
    print("SELFTEST: %d/%d traps oracle-fail" % (total - bad, total))
    return 1 if bad else 0


def oracle_check(arm):
    """Sanity: arms' real impls still PASS their oracles (run-state intact)."""
    bad = 0
    for fx in FIXTURES:
        arm_dir = os.path.join(RUNS, arm, fx)
        rc, out = run_py([oracle_path(fx), arm_dir], cwd=HERE)
        line = [l for l in out.splitlines() if l.startswith("ORACLE:")]
        print("%s/%s %s %s" % (arm, fx, "PASS" if rc == 0 else "FAIL",
                               line[-1] if line else "(no summary)"))
        bad += 0 if rc == 0 else 1
    print("ORACLE-CHECK %s: %d/%d pass" % (arm, len(FIXTURES) - bad, len(FIXTURES)))
    return 1 if bad else 0


def battery(arm, only=None):
    """Swap every trap into the arm dir, run the arm's OWN acceptance test."""
    fixtures = [only] if only else FIXTURES
    killed = survived = infra = 0
    total_traps = 0
    rows = []
    for fx in fixtures:
        mod = MODULES[fx]
        arm_dir = os.path.join(RUNS, arm, fx)
        mod_path = os.path.join(arm_dir, mod + ".py")
        test_name = "test_%s.py" % mod
        if not os.path.isfile(mod_path) or not os.path.isfile(os.path.join(arm_dir, test_name)):
            print("INFRA: %s/%s missing module or test" % (arm, fx))
            infra += 1
            continue
        fx_killed = 0
        traps = traps_for(fx)
        total_traps += len(traps)
        for trap in traps:
            before = sha(mod_path)
            bak = mod_path + ".battery-bak"
            shutil.copyfile(mod_path, bak)
            try:
                shutil.copyfile(os.path.join(HERE, "traps", fx, trap), mod_path)
                rc, _ = run_py([test_name], cwd=arm_dir)
            finally:
                shutil.copyfile(bak, mod_path)
                os.remove(bak)
            if sha(mod_path) != before:
                print("INFRA: restore hash mismatch %s/%s — ABORT" % (arm, fx))
                return 2
            if rc < 0:
                infra += 1
                verdict = "INFRA"
            elif rc == 0:
                survived += 1
                verdict = "SURVIVED"
            else:
                killed += 1
                fx_killed += 1
                verdict = "killed"
            rows.append("  %-28s %s" % (trap, verdict))
        rows.append("%s/%s trap-kill %d/%d" % (arm, fx, fx_killed, len(traps)))
    print("\n".join(rows))
    print("BATTERY %s: killed %d / %d (survived %d, infra %d) — trap-kill rate %.0f%%"
          % (arm, killed, total_traps, survived, infra,
             100.0 * killed / total_traps if total_traps else 0))
    return 0


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else ""
    if mode == "selftest":
        sys.exit(selftest())
    if mode == "oracle":
        sys.exit(oracle_check(sys.argv[2]))
    if mode == "run":
        sys.exit(battery(sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else None))
    print(__doc__)
    sys.exit(1)


if __name__ == "__main__":
    main()
