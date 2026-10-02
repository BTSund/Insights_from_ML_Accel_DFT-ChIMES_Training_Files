# Si ChIMES training inputs: PW91

Inputs used to fit the ChIMES silicon model trained to **PW91** DFT data.

## Files

| File | What it is |
|---|---|
| `fm_setup.in` | ChIMES-LSQ fit setup: 900 training frames, Si only, Chebyshev orders 2B/3B/4B = 20/12/3, Morse transform (λ = 2.33 Å), Tersoff cutoff (0.75), r = 1.55–7.0 Å (2B), 6.0 Å (3B), 5.0 Å (4B). Fits forces, energies and all stress components. `SPLITFI` = true. |
| `weights.txt` | Per-row weights for the least-squares design matrix (one value per force, energy and stress row), produced by `generate_weights.py`. Pass to the ChIMES `lsq2.py` solver. |
| `generate_weights.py` | Script that builds `weights.txt` (originally named `Updated_Abs.py`). |
| `config.py` | Config for the ChIMES PES scan utility (`pes_generator.py`) used to plot the fitted 2- and 3-body curves. Keep the name `config.py`; the utility imports it by that name. |

## How the weights are built (`generate_weights.py`)

Needs, in the working directory:

- `trajlist.dat`: the trajectory list referenced by `fm_setup.in` (first line = number of files, then one `.xyzf` path per line).
- `b-labeled.txt`: the labeled target vector written by `chimes_lsq` (row labels `Si` = force, `+1` = energy, `s_*` = stress).

Calculator commit:commit 3bc4d3c613bf0b01772bc13d532b64de071d3399
LSQ commit: 7567867fa85ae22d29c7f84f495149a11003df6b

Steps:

1. Reads every frame in the `.xyzf` files in `trajlist.dat` and computes each frame's mean |force|.
2. Splits the frames into groups (`group_sizes`; one group = one block of related configurations, in trajlist order; must sum to 900).
3. **Force weight** per group = median(|F| over all frames) / mean(|F| in group), capped at 5. Groups with small forces get more weight, so every group contributes about equally.
4. **Energy** and **stress** weights are set by hand per group (`energies`, `stresses` arrays).
5. Walks `b-labeled.txt` row by row and writes the matching weight to `weights.txt`.

If you add or remove frames, update `group_sizes`, `energies` and `stresses` to match, and update `NFRAMES` in `fm_setup.in`.

## Before reusing

- `config.py` contains absolute cluster paths (`CHMS_REPO`, `PARAM_FILE`). Point them at your ChIMES install and fitted `params.txt`.
- The training trajectories (`trajlist.dat` and the `.xyzf` files) are not included in this folder.
