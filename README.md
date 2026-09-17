# fsot-millennium-measured

Isolated **measured-compare lab** for Navier–Stokes, Birch–Swinnerton-Dyer, and Hodge. **Public** repository.

**FSOT 2.1** (`dappalumbo91/FSOT-2.1-Lean`, pin AEB2AD) is the authority for the mathematical system. This repo is a sandbox: run functions against public data, keep Clay theorems out of the scoreboard, then migrate findings back.

Not a Clay Prize claim. GitHub is not a Qualifying Outlet.

## License

**Apache License 2.0** — same as the Circuit lab. Better fit than MIT here: explicit patent grant, NOTICE/attribution for the vendored seed slice, and contribution terms when findings move back into FSOT 2.1.

## What is measured (and what is not)

| Track | Function with data | Clay remainder (no residual) |
|-------|--------------------|------------------------------|
| NSE | Stretch/visc cartoon vs 2D theorem, Euler, DNS phenomenology; Kolmogorov 4/5, 3/2, 1/3, κ | Smoothness on \(\mathbb{R}^3\) |
| BSD | Sha volume vs LMFDB on named curves | rank = ord \(L\) for every \(E\) |
| Hodge | \(\chi\) vs Chern on named varieties | Algebraicity without a named cycle |

## Run

```powershell
pip install -r requirements.txt
python measured/run_compares.py
```

Writes `results/measured_compares.json`.

## Kill

- Stuffing 4/5 or the cartoon into 3D smoothness
- Weierstrass → ℤ; Kato as a seed
- Hunting Hassett \(C_{48}\); stealing \(25-1\) for \(\chi(\mathrm{K3})\)
- Rewriting the H0 freeze
