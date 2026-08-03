"""Run every verification script in code/, in paper order. See README.md."""
import os
import pathlib
import subprocess
import sys
import time

SCRIPTS = [
    ("Paper 1 - u-space formula system (40-test suite)", "prime_sum_formula.py"),
    ("Paper 2 - certified Chebyshev ladder", "certified_snap.py"),
    ("Paper 3 - prime recovery, both routes", "prime_recovery.py"),
    ("Paper 4 - crystal demos (every table in the essay)", "crystal_demos.py"),
    ("Paper 4 - skeleton-null scanner", "untargeted_scan.py"),
    ("Paper 4 - graph universe column (WP9a)", "graph_universe.py"),
    ("Paper 4 - explicit-formula pairing (WP3)", "diffraction_pairing.py"),
    ("Programme Note 2 - formal engine checks", "formal_engine.py"),
]


def main():
    code = pathlib.Path(__file__).parent / "code"
    if "--list" in sys.argv:
        for label, name in SCRIPTS:
            print(f"{name:<24} {label}")
        return 0
    failures = []
    for label, name in SCRIPTS:
        print(f"\n{'=' * 72}\n== {label}  ({name})\n{'=' * 72}", flush=True)
        t0 = time.time()
        env = {**os.environ, "PYTHONIOENCODING": "utf-8"}
        result = subprocess.run([sys.executable, str(code / name)], env=env)
        print(f"-- exit {result.returncode} in {time.time() - t0:.1f}s")
        if result.returncode != 0:
            failures.append(name)
    print(f"\n{'=' * 72}")
    if failures:
        print("FAILED:", ", ".join(failures))
        return 1
    print("all verification scripts completed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
