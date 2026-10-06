# Effect-robustness arms added 2026-10-06

Three switches, each defaulting to the behaviour of every stored run:

| Parameter | Arm | Question |
|---|---|---|
| `platform_routing="loyal"` | `eff_routing_loyal_*` | How much do the stacking shares depend on random routing? |
| `shortfall_bnpl=False` | `eff_no_shortfall_bnpl_*` | How much of the BNPL effect runs through the shortfall path? |
| `committed_shortfall_funded=True` | `eff_committed_funded_*` | Does spending credit on an unpaid committed shortfall first change the result? |

`run_variants.py` re-ran the whole effect suite and asserted that all 880 stored runs are
reproduced exactly (largest absolute difference 0.0 over 127 columns; `run_variants.log`),
then saved the 140 new runs into `results/raw/effect.parquet`. Seeds 70,000 to 70,019, as for
the rest of the suite. The baseline is not recalibrated for any arm.

Results (`results_numbers.json`, rows of `tab_effect`): loyal routing cuts the share of
final-tick holders owing two or more platforms from 52.6% to 36.6% at beta=0 and from 85.2%
to 22.0% at beta=1 without a detectable change in default; removing BNPL from the shortfall
path leaves a detectable effect at beta=1 (0.47 +- 0.11); funding the committed shortfall
leaves the effect at 0.68 +- 0.11 at beta=1.

    PYTHONPATH=. .venv/bin/python -m pytest simulation/tests -q
    PYTHONPATH=. .venv/bin/python results/variants_2026-10-06/run_variants.py
    PYTHONPATH=. .venv/bin/python notebooks/scripts/build_results_tables.py
    PYTHONPATH=. .venv/bin/python notebooks/scripts/check_results_tables.py
