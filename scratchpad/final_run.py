"""Final-run driver: the three commands of OVERVIEW step 4, in order, stopping on failure.

    ./env/python.exe scratchpad/final_run.py [--skip-sobol]

Everything the three steps print goes to results/final_run.log, which ends with one of
two sentinel lines: `FINAL RUN COMPLETE` or `FINAL RUN FAILED at <step>`. The log opens
with the commit the run was produced from, so the results are traceable to the code.
"""
import argparse
import os
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOG = ROOT / "results" / "final_run.log"
STEPS = [
    ["-m", "simulation.experiments", "--which", "all", "--reps", "20"],
    ["-m", "simulation.sensitivity", "--samples", "256"],
    ["-m", "simulation.analysis"],
]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--skip-sobol", action="store_true", help="drop the sensitivity step")
    steps = [s for s in STEPS if not (parser.parse_args().skip_sobol and "simulation.sensitivity" in s)]
    env = {**os.environ, "PYTHONUNBUFFERED": "1", "PYTHONUTF8": "1"}
    commit = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True, text=True
    ).stdout.strip()
    dirty = subprocess.run(
        ["git", "status", "--porcelain", "--", "simulation", "data/config"],
        cwd=ROOT, capture_output=True, text=True,
    ).stdout.strip()

    with LOG.open("w", encoding="utf-8") as log:
        def say(line: str) -> None:
            log.write(line + "\n")
            log.flush()

        say(f"FINAL RUN started {datetime.now():%Y-%m-%d %H:%M:%S}")
        say(f"commit {commit}" + ("  (simulation/ or data/config has UNCOMMITTED changes)" if dirty else ""))
        for step in steps:
            name = " ".join(step)
            say(f"\n=== {datetime.now():%H:%M:%S}  python {name}")
            t0 = time.time()
            code = subprocess.run(
                [sys.executable, *step], cwd=ROOT, env=env, stdout=log, stderr=subprocess.STDOUT
            ).returncode
            say(f"=== exit {code} after {(time.time() - t0) / 60:.1f} min")
            if code:
                say(f"FINAL RUN FAILED at {name}")
                return code
        say(f"FINAL RUN COMPLETE {datetime.now():%Y-%m-%d %H:%M:%S}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
