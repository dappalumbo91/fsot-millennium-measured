# Gauntlet stamp — measured lab

**When:** 2026-09-17  
**Authority:** FSOT 2.1 Lean pin AEB2AD  
**Lab run:** `python scripts/reproduce.py`  
**Clay prize claimed:** false

## Measured compares

| Track | Result |
|-------|--------|
| NSE 3D viscous Taylor–Green | stretching 3D, damps at seed μ; Euler μ=0 is the wrong orifice |
| NSE ω0 scan vs Riccati threshold | 6/6 |
| BSD Sha vs LMFDB named curves | 17/17 |
| Hodge χ vs Chern | 9/9 |

## Uniqueness gauntlet (in this repo, not Python-only)

153 obligations, same spine as FSOT 2.1: Python decimal, Rust f64, Z3 SMT, Coq, Isabelle, F*, TLA+, Lean `UniquenessResearchSpine`.

Clean-clone stamp: `data/reproduce_stamp.json`.

Public: https://github.com/dappalumbo91/fsot-millennium-measured
