#!/usr/bin/env python3
"""Clone-and-run stamp: millenium track + accuracy + measured compares + uniqueness gauntlet.

Usage (from repo root):
  pip install -r requirements.txt
  python scripts/reproduce.py
"""
from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "data" / "reproduce_stamp.json"


def _run(name: str, args: list[str], timeout: int = 1200) -> dict:
    print(f"\n=== {name} ===")
    r = subprocess.run(args, cwd=str(ROOT), timeout=timeout)
    ok = r.returncode == 0
    print(f"{name}: {'PASS' if ok else 'FAIL'} (exit {r.returncode})")
    return {"name": name, "ok": ok, "returncode": r.returncode}


def main() -> int:
    py = sys.executable
    steps = [
        _run("millennium_track", [py, str(ROOT / "vendor" / "fsot_millennium_track.py")]),
        _run("millennium_accuracy", [py, str(ROOT / "vendor" / "fsot_millennium_accuracy.py")], timeout=300),
        _run("measured_compares", [py, str(ROOT / "measured" / "run_compares.py")], timeout=300),
        _run(
            "uniqueness_gauntlet",
            [py, str(ROOT / "scripts" / "run_uniqueness_research_verification.py")],
            timeout=1200,
        ),
    ]
    overall = all(s["ok"] for s in steps)
    uniq = {}
    up = ROOT / "data" / "uniqueness_research_verification_report.json"
    if up.is_file():
        uniq = json.loads(up.read_text(encoding="utf-8"))
    acc = {}
    ap = ROOT / "data" / "millennium_accuracy_scoreboard.json"
    if ap.is_file():
        acc = json.loads(ap.read_text(encoding="utf-8"))
    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "pin": "AEB2AD",
        "overall_ok": overall,
        "clay_prize_claimed": False,
        "steps": steps,
        "millennium_accuracy": {
            "comparable_count": acc.get("comparable_count"),
            "beats_or_meets_count": acc.get("beats_or_meets_count"),
            "fsot_green_pass_n": acc.get("fsot_green_pass_n"),
            "clay_problems_remaining": acc.get("clay_problems_remaining"),
        },
        "uniqueness": {
            "obligation_count": uniq.get("obligation_count"),
            "python": (uniq.get("python_decimal") or {}).get("status"),
            "rust": (uniq.get("rust_f64_replay") or {}).get("status"),
            "smt": (uniq.get("smt_z3") or {}).get("status"),
            "coq": (uniq.get("coq_uniqueness") or {}).get("status"),
            "isabelle": (uniq.get("isabelle_uniqueness") or {}).get("status"),
            "fstar": (uniq.get("fstar") or {}).get("status"),
            "overall_ok": uniq.get("overall_ok"),
        },
    }
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"\nWrote {REPORT} overall_ok={overall}")
    return 0 if overall else 1


if __name__ == "__main__":
    raise SystemExit(main())
