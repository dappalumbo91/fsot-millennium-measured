# fsot-millennium-measured

Public **measured-compare + millenium gauntlet** lab for Navier–Stokes, Birch–Swinnerton-Dyer, and Hodge.

**FSOT 2.1** (`dappalumbo91/FSOT-2.1-Lean`, pin AEB2AD) is the authority for the mathematical system. This repo vendors the millenium/uniqueness slice so a clean clone can reproduce the stamp. Findings migrate back. Not a Clay Prize. GitHub is not a Qualifying Outlet.

This is **not a Python-only dump**. The uniqueness gauntlet is checked in as:

| Language | Path |
|----------|------|
| Python decimal | `vendor/fsot_uniqueness_confinement.py` |
| Rust f64 replay | `verification/rust/fsot_uniqueness_research_replay/` |
| Z3 SMT | `verification/smt/uniqueness_research_bounds.smt2` |
| Coq | `verification/coq/UniquenessResearchSpine.v` |
| Isabelle | `verification/isabelle/UniquenessResearchSpine.thy` |
| F\* | `verification/fstar/FSOTUniquenessResearch.fst` |
| TLA+ | `verification/tla/FSOTUniquenessResearch.tla` |
| Lean | `FSOT/Formal/UniquenessResearchSpine.lean` |

**147 uniqueness obligations** regenerated from the vendored millenium slice. FSOT 2.1's authority gauntlet is 153; the extra six are market/sickness flags that live in 2.1, not this lab. `python scripts/reproduce.py` runs Python plus every prover found on `PATH`.

## License

Apache-2.0 (patent grant + NOTICE for the vendored seed slice).

## Clone and reproduce

Needs: Python 3.11+, `mpmath`, `numpy`. Optional for the uniqueness gauntlet: Rust/`cargo`, Z3, Coq, Isabelle, F\* (the runner uses whatever is on `PATH`).

```powershell
git clone https://github.com/dappalumbo91/fsot-millennium-measured.git
cd fsot-millennium-measured
pip install -r requirements.txt
python scripts/reproduce.py
```

That runs, in order:

1. `vendor/fsot_millennium_track.py` — Clay process flags (all still open)
2. `vendor/fsot_millennium_accuracy.py` — scoreboard vs observables
3. `measured/run_compares.py` — 3D TG NSE, Sha panel, χ panel
4. `scripts/run_uniqueness_research_verification.py` — Python / Rust / Z3 / Coq / Isabelle / F\*

Stamp: `data/reproduce_stamp.json` (`overall_ok` true/false). Clay remains unclaimed.

Docs: `docs/MILLENNIUM_{NSE,BSD,HODGE,YM,PRIZE,ACCURACY,MEASURED_LAB}*.md`, named outcomes in `results/millennium_named_outcomes.md`.

## What is measured (observables, not rival theories)

| Track | Function with data | Clay remainder |
|-------|--------------------|----------------|
| NSE | CRC/NIST/US1976 lab tables; 3D viscous Taylor–Green on \(\mathbb{T}^3\) | Smoothness on \(\mathbb{R}^3\) |
| BSD | Sha vs LMFDB named curves; MW generators; 11a1 torsion | rank = ord \(L\) for every \(E\) |
| Hodge | \(\chi\) of named varieties vs Chern | Algebraicity without a named cycle |

## Kill

- Stuffing 4/5 or a cartoon into 3D smoothness
- Using Euler \(\mu=0\) as the lab bar
- Weierstrass → ℤ; Kato as a seed
- Hunting Hassett \(C_{48}\); stealing \(25-1\) for \(\chi(\mathrm{K3})\)
- Rewriting the H0 freeze
