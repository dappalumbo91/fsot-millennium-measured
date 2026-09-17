# Findings to migrate back to FSOT 2.1

Pin AEB2AD. Clay not claimed.

1. **3D NSE on T^3** (spectral Taylor–Green, seed μ): stretching production is 3D. Viscous run damps energy and max|ω|. 3D Euler on the same grid does not dissipate (max|ω| grows). Not 2D. Not Clay on R^3.
2. **NSE stretch/visc cartoon** (α=POOF, μ=μ(Fluid)): ω0 scan vs Riccati threshold **6/6**. Not a substitute for the 3D spectral run.

2. **BSD Sha panel** vs LMFDB named curves: **17/17** Sha_an=1. Not rank=ord L for every E.

3. **Hodge χ panel** vs Chern: **9/9** including quintic 4-fold χ=825 (same hypersurface family, not Hassett C_48).

Migrate these into `vendor/fsot_millennium_accuracy.py` when ready. Do not rewrite the H0 freeze.
