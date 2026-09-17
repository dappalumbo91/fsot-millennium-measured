#!/usr/bin/env python3
"""Measured compares for NSE / BSD / Hodge. Not Clay theorems.

Run from repo root: python measured/run_compares.py
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "vendor"))
sys.path.insert(0, str(ROOT / "measured"))

from fsot_dynamics import nse_stretch_integrate, nse_stretch_sim_panel, viscosity_eff  # noqa: E402
from fsot_nse3d import nse3d_measured_compare  # noqa: E402
from fsot_compute import POOF, derived_D_eff  # noqa: E402
from fsot_seed_flavor import (  # noqa: E402
    bsd_analytic_sha,
    seed_abelian_4fold_euler,
    seed_cp2_euler,
    seed_cp2xcp2_euler,
    seed_cp3_euler,
    seed_cubic_4fold_euler,
    seed_gr24_euler,
    seed_hypersurface_4fold_euler,
    seed_kolmogorov_45,
    seed_kolmogorov_d2_32,
    seed_onsager_holder,
    seed_quartic_4fold_euler,
    seed_sextic_4fold_euler,
    seed_von_karman,
)
from lmfdb_bsd import CURVES  # noqa: E402

OUT = ROOT / "results" / "measured_compares.json"
VON_KARMAN = 0.40


def _nse() -> dict:
    panel = nse_stretch_sim_panel()
    mu = float(panel["mu"])
    alpha = float(panel["alpha_3d"])
    thresh = mu / max(alpha, 1e-30)
    scan = []
    hits = 0
    for scale in (0.25, 0.5, 0.9, 1.0, 1.1, 2.0):
        w0 = thresh * scale
        run = nse_stretch_integrate(alpha, mu, omega0=w0)
        predicted_finite = w0 <= thresh * (1.0 + 1e-12)
        agree = bool(run["finite"]) == predicted_finite
        hits += int(agree)
        scan.append(
            {
                "omega0": w0,
                "scale_of_threshold": scale,
                "finite": bool(run["finite"]),
                "predicted_finite": predicted_finite,
                "agree": agree,
            }
        )
    identities = {
        "kolmogorov_45": seed_kolmogorov_45(),
        "kraichnan_32": seed_kolmogorov_d2_32(),
        "onsager_13": seed_onsager_holder(),
        "von_karman": seed_von_karman(),
        "von_karman_vs_040_pct": abs(seed_von_karman() - VON_KARMAN) / VON_KARMAN * 100.0,
    }
    return {
        "cartoon_vs_public_answers": {
            "2d_finite": panel["two_d_finite"],
            "euler_finite": panel["euler_finite"],
            "nse3_finite": panel["nse3_finite"],
            "agrees_2d_proven_regular": panel["agrees_2d_proven_regular"],
            "agrees_euler_more_singular": panel["agrees_euler_more_singular"],
            "agrees_dns_no_blowup_accessible_Re": panel["agrees_dns_no_blowup_accessible_Re"],
            "public_2d_answer": panel["public_2d_answer"],
            "public_euler_answer": panel["public_euler_answer"],
            "public_dns_answer": panel["public_dns_answer"],
            "clay_claimed": False,
        },
        "omega0_scan_vs_riccati_threshold": {
            "threshold": thresh,
            "mu": mu,
            "alpha": alpha,
            "hits": hits,
            "n": len(scan),
            "hit_pct": 100.0 * hits / len(scan),
            "rows": scan,
        },
        "identities_vs_public": identities,
        "nse3d_taylor_green": nse3d_measured_compare(),
        "clay": "not_claimed",
    }


def _bsd() -> dict:
    hits = 0
    rows = []
    for lab, lead, om, tam, tors, reg in CURVES:
        sha = bsd_analytic_sha(lead, om, tam, tors, reg)
        err = abs(sha - 1.0) / 1.0 * 100.0
        ok = err < 0.5
        hits += int(ok)
        rows.append({"label": lab, "sha": sha, "err_pct_vs_1": err, "hit": ok})
    n = len(CURVES)
    return {
        "hits": hits,
        "n": n,
        "hit_pct": 100.0 * hits / n,
        "rows": rows,
        "clay": "not_claimed",
        "note": "Volume function vs LMFDB Sha_an=1 on named curves. Not rank=ord L for every E.",
    }


def _hodge() -> dict:
    pairs = [
        ("CP2", seed_cp2_euler(), 3.0),
        ("CP3", seed_cp3_euler(), 4.0),
        ("CP2xCP2", seed_cp2xcp2_euler(), 9.0),
        ("Gr24", seed_gr24_euler(), 6.0),
        ("cubic4", seed_cubic_4fold_euler(), 27.0),
        ("quartic4", seed_quartic_4fold_euler(), 188.0),
        ("quintic4", seed_hypersurface_4fold_euler(5), 825.0),
        ("sextic4_CY", seed_sextic_4fold_euler(), 2610.0),
        ("abelian4", seed_abelian_4fold_euler(), 0.0),
    ]
    rows = []
    hits = 0
    for name, got, want in pairs:
        ok = abs(got - want) < 1e-9
        hits += int(ok)
        rows.append({"name": name, "computed": got, "measured": want, "hit": ok})
    n = len(pairs)
    return {
        "hits": hits,
        "n": n,
        "hit_pct": 100.0 * hits / n,
        "rows": rows,
        "clay": "not_claimed",
        "note": "chi vs Chern/literature on named varieties. Quintic d=5 is the same hypersurface family, not Hassett C_48.",
    }


def main() -> int:
    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "pin": "AEB2AD",
        "clay_prize_claimed": False,
        "license": "Apache-2.0",
        "authority": "FSOT-2.1-Lean",
        "nse": _nse(),
        "bsd": _bsd(),
        "hodge": _hodge(),
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    nse = payload["nse"]
    print("NSE cartoon vs public answers:")
    print("  2D finite", nse["cartoon_vs_public_answers"]["2d_finite"], "↔ proven global")
    print("  Euler finite", nse["cartoon_vs_public_answers"]["euler_finite"], "↔ more singular")
    print("  NSE3 finite", nse["cartoon_vs_public_answers"]["nse3_finite"], "↔ DNS no blow-up at accessible Re")
    scan = nse["omega0_scan_vs_riccati_threshold"]
    print(f"  omega0 scan vs threshold: {scan['hits']}/{scan['n']} ({scan['hit_pct']:.1f}%)")
    tg = nse["nse3d_taylor_green"]
    print(
        "  3D viscous TG",
        tg["agrees_3d_viscous_tg_dns_decay"],
        "stretching_3d",
        tg["stretching_is_3d"],
        "ok",
        tg["ok"],
        "(Euler μ=0 is wrong orifice)",
    )
    print(f"BSD Sha vs LMFDB: {payload['bsd']['hits']}/{payload['bsd']['n']}")
    print(f"Hodge chi vs Chern: {payload['hodge']['hits']}/{payload['hodge']['n']}")
    print("clay_prize_claimed", payload["clay_prize_claimed"])
    print("wrote", OUT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
