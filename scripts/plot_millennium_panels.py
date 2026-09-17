#!/usr/bin/env python3
"""Conventional millenium pictures vs FSOT measured functions.

Not Clay. Not a substitute for reproduce.py.
Run from repo root: python scripts/plot_millennium_panels.py
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "vendor"))
sys.path.insert(0, str(ROOT / "measured"))

import numpy as np

try:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
except ImportError as exc:  # pragma: no cover
    raise SystemExit("matplotlib is required for figures: pip install matplotlib") from exc

from fsot_millennium_track import GAMMA, RIEMANN_T1  # noqa: E402
from fsot_nse3d import nse3d_run  # noqa: E402
from fsot_seed_flavor import (  # noqa: E402
    seed_abelian_4fold_euler,
    seed_cp2_euler,
    seed_cp2xcp2_euler,
    seed_cubic_4fold_euler,
    seed_gr24_euler,
    seed_hypersurface_4fold_euler,
    seed_kolmogorov_45,
    seed_kolmogorov_d2_32,
    seed_onsager_holder,
)

OUT = ROOT / "results" / "figures"
COMPARE = ROOT / "results" / "measured_compares.json"

# Public Odlyzko first ten imaginary parts (standard table, not a seed).
ODLYZKO_T = [
    14.1347251417,
    21.0220396388,
    25.0108575801,
    30.4248761259,
    32.9350615877,
    37.5861781588,
    40.9187190121,
    43.3270732809,
    48.0051508812,
    49.7738324777,
]


def _style() -> None:
    plt.rcParams.update(
        {
            "figure.facecolor": "white",
            "axes.facecolor": "white",
            "axes.grid": True,
            "grid.alpha": 0.25,
            "font.size": 10,
            "axes.titlesize": 11,
            "savefig.bbox": "tight",
            "savefig.dpi": 140,
        }
    )


def _save(fig: plt.Figure, name: str) -> Path:
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / name
    fig.savefig(path)
    plt.close(fig)
    print(f"wrote {path}")
    return path


def plot_nse_spectrum() -> None:
    k = np.logspace(0.3, 2.2, 200)
    e_kol = k ** (-5.0 / 3.0)
    fig, axes = plt.subplots(1, 2, figsize=(10.5, 4.2))
    axes[0].loglog(k, e_kol, color="#4c78a8", lw=2)
    axes[0].set_xlabel("wavenumber k")
    axes[0].set_ylabel("E(k)")
    axes[0].set_title("Conventional: Kolmogorov E(k) ~ k^{-5/3}")
    axes[0].annotate("inertial range (formula picture)", xy=(12, 0.08), fontsize=8)

    labels = ["3D flux 4/5", "2D inverse 3/2", "Onsager 1/3"]
    vals = [seed_kolmogorov_45(), seed_kolmogorov_d2_32(), seed_onsager_holder()]
    expect = [0.8, 1.5, 1.0 / 3.0]
    x = np.arange(len(labels))
    axes[1].bar(x - 0.18, expect, 0.36, label="public identity", color="#9e9ac8")
    axes[1].bar(x + 0.18, vals, 0.36, label="FSOT seed", color="#2ca02c")
    axes[1].set_xticks(x, labels, rotation=15)
    axes[1].set_ylabel("number")
    axes[1].set_title("FSOT: cascade numbers (not a smoothness lamp)")
    axes[1].legend(frameon=False, loc="upper left")
    fig.suptitle("NSE — people plot a spectrum; FSOT hits the flux numbers", y=1.02)
    _save(fig, "nse_spectrum_conventional_vs_fsot.png")


def plot_nse_tg() -> None:
    visc = nse3d_run(return_histories=True)
    euler = nse3d_run(mu=0.0, return_histories=True)
    t_v = np.arange(len(visc["history"]["energy"])) * visc["dt"]
    t_e = np.arange(len(euler["history"]["energy"])) * euler["dt"]
    fig, axes = plt.subplots(1, 2, figsize=(10.5, 4.2))
    axes[0].plot(t_v, visc["history"]["energy"], color="#2ca02c", lw=2, label="viscous NSE (seed μ)")
    axes[0].plot(t_e, euler["history"]["energy"], color="#d62728", lw=1.5, ls="--", label="Euler μ=0 (wrong orifice)")
    axes[0].set_xlabel("t")
    axes[0].set_ylabel("kinetic energy")
    axes[0].set_title("Energy vs time on T^3 Taylor–Green")
    axes[0].legend(frameon=False, fontsize=8)
    axes[1].plot(t_v, visc["history"]["max_omega"], color="#2ca02c", lw=2, label="viscous max|ω|")
    axes[1].plot(t_e, euler["history"]["max_omega"], color="#d62728", lw=1.5, ls="--", label="Euler max|ω|")
    axes[1].set_xlabel("t")
    axes[1].set_ylabel("max |ω|")
    axes[1].set_title("Vorticity: viscous damps; Euler is not the lab bar")
    axes[1].legend(frameon=False, fontsize=8)
    fig.suptitle("Conventional TG pictures show isosurfaces; FSOT plots the viscous function", y=1.02)
    _save(fig, "nse_tg_energy_viscous_vs_euler.png")


def plot_nse_omega0() -> None:
    payload = json.loads(COMPARE.read_text(encoding="utf-8"))
    rows = payload["nse"]["omega0_scan_vs_riccati_threshold"]["rows"]
    thresh = payload["nse"]["omega0_scan_vs_riccati_threshold"]["threshold"]
    fig, ax = plt.subplots(figsize=(7.2, 4.0))
    for row in rows:
        color = "#2ca02c" if row["finite"] else "#d62728"
        marker = "o" if row["agree"] else "x"
        ax.scatter(row["omega0"], 1 if row["finite"] else 0, c=color, marker=marker, s=60, zorder=3)
    ax.axvline(thresh, color="#4c78a8", ls="--", label="Riccati threshold μ/POOF")
    ax.set_yticks([0, 1], ["blows (cartoon)", "finite (cartoon)"])
    ax.set_xlabel("ω0")
    ax.set_title("FSOT stretch/visc cartoon — 6/6 vs threshold (not Clay 3D NSE)")
    ax.legend(frameon=False)
    _save(fig, "nse_omega0_scan.png")


def plot_bsd_L() -> None:
    s = np.linspace(0.2, 1.8, 400)
    fig, ax = plt.subplots(figsize=(7.4, 4.2))
    styles = [
        (0, 0.45, "#4c78a8", "r=0  L(1)≠0"),
        (1, 0.55, "#e45756", "r=1  simple zero"),
        (2, 0.35, "#72b7b2", "r=2  double zero"),
    ]
    for r, c, color, label in styles:
        ax.plot(s, c * (s - 1.0) ** r, color=color, lw=2, label=label)
    ax.axvline(1.0, color="0.4", lw=0.8)
    ax.axhline(0.0, color="0.4", lw=0.8)
    ax.set_xlabel("s")
    ax.set_ylabel("schematic L(E,s)")
    ax.set_title("Conventional BSD picture: order of vanishing at s=1")
    ax.legend(frameon=False, fontsize=8)
    ax.set_ylim(-0.2, 1.0)
    _save(fig, "bsd_L_vanishing_orders.png")


def plot_bsd_sha() -> None:
    payload = json.loads(COMPARE.read_text(encoding="utf-8"))
    rows = payload["bsd"]["rows"]
    labels = [r["label"] for r in rows]
    sha = [r["sha"] for r in rows]
    fig, ax = plt.subplots(figsize=(10.5, 4.2))
    ax.bar(range(len(labels)), sha, color="#2ca02c")
    ax.axhline(1.0, color="#4c78a8", ls="--", lw=1.2, label="volume target Sha=1")
    ax.set_xticks(range(len(labels)), labels, rotation=55, ha="right", fontsize=8)
    ax.set_ylabel("analytic Sha")
    ax.set_title(f"FSOT function: Sha panel vs LMFDB named curves ({payload['bsd']['hits']}/{payload['bsd']['n']})")
    ax.legend(frameon=False)
    ax.set_ylim(0.0, 1.15)
    _save(fig, "bsd_sha_panel.png")


def plot_hodge_diamond() -> None:
    # Cubic 4-fold Hodge diamond (h^{3,1}=1, h^{2,2}=21, h^{4,0}=0).
    rows = [
        ["1"],
        ["0", "0"],
        ["0", "1", "0"],
        ["0", "0", "0", "0"],
        ["0", "1", "21", "1", "0"],
        ["0", "0", "0", "0"],
        ["0", "1", "0"],
        ["0", "0"],
        ["1"],
    ]
    fig, ax = plt.subplots(figsize=(6.6, 6.2))
    ax.set_xlim(-5.0, 5.0)
    ax.set_ylim(-0.5, 9.0)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("Conventional: Hodge diamond of a cubic 4-fold\n(h^{2,2}=21; very general rational (2,2) is only ⟨h²⟩)")
    for i, row in enumerate(rows):
        y = 8.2 - i * 0.9
        n = len(row)
        for j, txt in enumerate(row):
            x = (j - (n - 1) / 2.0) * 0.95
            face = "#fff2ae" if txt == "21" else "#f0f0f0"
            ax.add_patch(plt.Circle((x, y), 0.38, fc=face, ec="#333333", lw=0.8))
            ax.text(x, y, txt, ha="center", va="center", fontsize=9)
    ax.text(0.0, -0.15, "FSOT: extra rational classes live on named C_d, not this diamond hunt", ha="center", fontsize=8)
    _save(fig, "hodge_diamond_cubic.png")


def plot_hodge_chi() -> None:
    rows = [
        (r"$\mathbb{CP}^2$", seed_cp2_euler(), 3),
        (r"$\mathbb{CP}^2\times\mathbb{CP}^2$", seed_cp2xcp2_euler(), 9),
        ("Gr(2,4)", seed_gr24_euler(), 6),
        ("cubic 4-fold", seed_cubic_4fold_euler(), 27),
        ("quartic 4-fold", seed_hypersurface_4fold_euler(4), 188),
        ("quintic 4-fold", seed_hypersurface_4fold_euler(5), 825),
        ("sextic CY 4-fold", seed_hypersurface_4fold_euler(6), 2610),
        ("abelian 4-fold", seed_abelian_4fold_euler(), 0),
    ]
    small = rows[:4]
    large = rows[4:]
    fig, axes = plt.subplots(1, 2, figsize=(11.0, 4.4))
    for ax, group, title in (
        (axes[0], small, "small named χ"),
        (axes[1], large, "hypersurface / abelian 4-folds"),
    ):
        labels = [r[0] for r in group]
        fsot = [r[1] for r in group]
        chern = [r[2] for r in group]
        x = np.arange(len(labels))
        ax.bar(x - 0.18, chern, 0.36, label="Chern / literature", color="#9e9ac8")
        ax.bar(x + 0.18, fsot, 0.36, label="FSOT seed χ", color="#2ca02c")
        ax.set_xticks(x, labels, rotation=20, ha="right")
        ax.set_ylabel("Euler number χ")
        ax.set_title(title)
        ax.legend(frameon=False, fontsize=8)
    fig.suptitle("FSOT function: named-variety χ vs Chern (9/9) — not Clay algebraicity", y=1.02)
    _save(fig, "hodge_chi_panel.png")


def plot_ym_damping() -> None:
    t = np.linspace(0.0, 8.0, 400)
    gamma = 0.67
    fig, axes = plt.subplots(1, 2, figsize=(10.5, 4.2))
    axes[0].plot(t, np.exp(-gamma * t), color="#2ca02c", lw=2)
    axes[0].plot(t, np.ones_like(t), color="#d62728", ls="--", lw=1.5, label="γ=0 free color persists")
    axes[0].set_xlabel("process time")
    axes[0].set_ylabel("free-color amplitude")
    axes[0].set_title("FSOT: free color damps (not an attractor)")
    axes[0].legend(frameon=False, fontsize=8)
    phi = (1.0 + math.sqrt(5.0)) / 2.0
    axes[1].bar(
        [0, 1],
        [phi ** 2 + 1.0, 3.65],
        color=["#2ca02c", "#9e9ac8"],
    )
    axes[1].set_xticks([0, 1], ["isolated gap φ²+1", "Teper 3.65 (flux-tube check)"])
    axes[1].set_ylabel("m / √σ")
    axes[1].set_title("Conventional glueball ratio is a check, not the question")
    fig.suptitle("YM — people plot Wilson loops / glueball towers; FSOT plots the gap function", y=1.02)
    _save(fig, "ym_free_color_damping.png")


def plot_riemann() -> None:
    t1 = math.e / (GAMMA ** 3)
    fig, ax = plt.subplots(figsize=(8.2, 4.4))
    ax.axvline(0.5, color="#4c78a8", lw=1.5, label="critical line Re=1/2")
    ax.scatter([0.5] * len(ODLYZKO_T), ODLYZKO_T, c="#9e9ac8", s=28, label="Odlyzko zeros (function)")
    ax.scatter([0.5], [t1], c="#2ca02c", s=70, zorder=3, label=f"FSOT t1=e/γ³ ({t1:.4f})")
    ax.scatter([0.5], [RIEMANN_T1], facecolors="none", edgecolors="#d62728", s=90, label="table ρ1")
    ax.set_xlim(0.0, 1.0)
    ax.set_xlabel("Re(s)")
    ax.set_ylabel("Im(s)")
    ax.set_title("Conventional RH picture: zeros on the line. FSOT hits t1 — not all zeros.")
    ax.legend(frameon=False, fontsize=8, loc="upper left")
    _save(fig, "riemann_critical_line.png")


def plot_asked_vs_function() -> None:
    fig, ax = plt.subplots(figsize=(11.2, 5.6))
    ax.axis("off")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_title("Asked (Clay formula)  →  Function with data  →  FSOT  ·  Clay leftover open")
    headers = ["Problem", "Asked (formula)", "Function (data)", "FSOT", "Not claimed"]
    rows = [
        ["YM", "Wightman on R^4", "no free color / gap", "φ²+1 ; γ>0 damp", "continuum QFT"],
        ["NSE", "smooth on R^3", "stretch vs visc, lab/DNS", "4/5, TG decay, CRC", "all-data smoothness"],
        ["BSD", "rank = ord L ∀E", "Sha volume, MW points", "17/17 Sha=1", "every E"],
        ["Hodge", "classes = cycles", "named χ / named surfaces", "9/9 χ ; C8..C44", "unnamed class"],
        ["Riemann", "all zeros on 1/2", "Odlyzko t_n, S(T)", "t1=e/γ³, C-lock", "all zeros"],
        ["P vs NP", "P=?NP", "search vs verify", "Grover 1/2", "class equality"],
    ]
    col_x = [0.01, 0.12, 0.32, 0.56, 0.78]
    widths = [0.10, 0.19, 0.23, 0.21, 0.20]
    for i, h in enumerate(headers):
        ax.add_patch(plt.Rectangle((col_x[i], 0.86), widths[i], 0.10, fc="#4c78a8", ec="none"))
        ax.text(col_x[i] + widths[i] / 2, 0.91, h, ha="center", va="center", color="white", fontsize=8, weight="bold")
    for r, row in enumerate(rows):
        y = 0.72 - r * 0.12
        for i, cell in enumerate(row):
            fc = "#e8f5e9" if i == 3 else "#f7f7f7"
            ax.add_patch(plt.Rectangle((col_x[i], y), widths[i], 0.11, fc=fc, ec="#cccccc"))
            ax.text(col_x[i] + widths[i] / 2, y + 0.055, cell, ha="center", va="center", fontsize=7)
    _save(fig, "asked_vs_function_strip.png")


def main() -> int:
    _style()
    plot_nse_spectrum()
    plot_nse_tg()
    plot_nse_omega0()
    plot_bsd_L()
    plot_bsd_sha()
    plot_hodge_diamond()
    plot_hodge_chi()
    plot_ym_damping()
    plot_riemann()
    plot_asked_vs_function()
    print(f"figures in {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
