# Findings to migrate back to FSOT 2.1

Pin AEB2AD. Clay not claimed.

1. **NSE stretch/visc cartoon** (α=POOF, μ=μ(Fluid)): 2D stays regular (agrees proven global); Euler toy blows; 3D NSE toy damps when ω0 ≤ μ/POOF. ω0 scan vs Riccati threshold **6/6**. DNS-style answer: no blow-up at accessible Re. Not 3D NSE on R^3.

2. **BSD Sha panel** vs LMFDB named curves: **17/17** Sha_an=1. Not rank=ord L for every E.

3. **Hodge χ panel** vs Chern: **9/9** including quintic 4-fold χ=825 (same hypersurface family, not Hassett C_48).

Migrate these into `vendor/fsot_millennium_accuracy.py` when ready. Do not rewrite the H0 freeze.
