# Gauntlet stamp — measured lab

**When:** 2026-09-17T21:24:36Z  
**Authority:** FSOT 2.1 Lean pin AEB2AD  
**Verified by:** clean clone of `https://github.com/dappalumbo91/fsot-millennium-measured` @ 6099992 then `python scripts/reproduce.py`  
**overall_ok:** true  
**Clay prize claimed:** false

## Millenium (top to bottom)

| Step | Result |
|------|--------|
| millenium_track | PASS |
| millenium_accuracy | PASS — comparable 70, beats 73, green 67, Clay remaining 6 |
| measured_compares | PASS — 3D viscous TG; Sha 17/17; χ 9/9; Euler μ=0 wrong orifice |
| uniqueness_gauntlet | PASS — 147/147 Python, Rust, Z3, Coq, Isabelle, F* |

## Uniqueness gauntlet (in this repo, not Python-only)

147 obligations regenerated from the vendored millenium slice (Lean / Coq / Isabelle / F* / Rust / SMT / TLA+). FSOT 2.1's 153 includes six market/sickness flags that are not this lab.

Stamp: `data/reproduce_stamp.json`.

Public: https://github.com/dappalumbo91/fsot-millennium-measured
