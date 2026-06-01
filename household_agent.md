# The Household Agent — Data → Agent Mapping

*How survey data becomes one agent in the model. Built for a supervisor walkthrough.
Everything is in **2017 units** — see [`OVERVIEW.md`](OVERVIEW.md) for the full strategy.*

---

## The idea in one sentence

Each **household agent** is a real **NIDS Wave 5 (2017)** household, given a **balance sheet** and
an **income-quintile tag**, then enriched with **financial-inclusion flags matched in from
FinScope**.

```
  NIDS W5 household row ──┐
  (income, spend, debt)   ├──►  Household Agent  (balance sheet + flags + quintile)
  FinScope flags ─────────┘
   (matched by quintile)
```

No invented people, no inflation maths: the numbers stay in 2017 Rands.

---

## The agent at a glance

```
                    ┌──────────────────────────────────────┐
                    │           HOUSEHOLD AGENT             │
                    ├──────────────────────────────────────┤
   INFLOW    ──►    │  income_monthly      (+ source)       │   from NIDS
                    │                                       │
   OUTFLOW   ──►    │  expenditure_committed                │   from NIDS
                    │  expenditure_discretionary            │
                    ├──────────────────────────────────────┤
   ASSETS    ──►    │  liquid_savings                       │   from NIDS
   LIABILITIES ─►   │  D_trad  +  monthly_trad_repayment    │
                    ├──────────────────────────────────────┤
   FLAGS     ──►    │  banked / credit / savings / informal │   from FinScope (matched)
                    ├──────────────────────────────────────┤
   TAGS      ──►    │  income_quintile (Q1–Q5)              │
                    │  size, composition, head demographics │   from NIDS
                    └──────────────────────────────────────┘
```

---

## The mapping table

All money in **2017 Rands — no CPI**. NIDS file: `data/raw/NIDS_W5/hhderived.csv`.
FinScope flags attached via the simple quintile cell-donor match.

| Agent field                   | Plain meaning                          | Source → column(s)                                                   |
| ----------------------------- | -------------------------------------- | ------------------------------------------------------------------- |
| `income_monthly`              | Money in each month                    | NIDS `w5_hhincome`                                                   |
| `income_source`               | Where most of it comes from            | NIDS `w5_hhwage` / `w5_hhgovt` / `w5_hhremitt` / … → WAGE/GRANT/OTHER |
| `expenditure_committed`       | Must-pay spending (food + rent)        | NIDS `w5_expf` + `w5_rentexpend`                                     |
| `expenditure_discretionary`   | Flexible spending                      | NIDS `w5_expnf` − `w5_rentexpend` (≥ 0)                              |
| `liquid_savings`              | Cash buffer                            | NIDS `w5_f_ass` (proxy — weak field)                                |
| `D_trad`                      | Traditional debt owed                  | NIDS `w5_f_deb`                                                      |
| `monthly_trad_repayment`      | Monthly debt payment                   | derived from `D_trad` (servicing rate)                              |
| `banked_status`               | Banked / underbanked / unbanked        | **FinScope (matched)**                                              |
| `credit_access_formal`        | Has formal credit                      | **FinScope (matched)**                                              |
| `savings_product`             | Holds a savings product                | **FinScope (matched)**                                              |
| `informal_finance`            | Mashonisa / stokvel / insurance        | **FinScope (matched)**                                              |
| `income_quintile`             | Which fifth of the income distribution | NIDS `w5_hhincome` + `w5_wgt` (weighted) — also the **match key**   |
| `household_size`              | How many people                        | NIDS `w5_hhsizer`                                                    |
| `household_composition`       | Adults / children / elderly            | NIDS member records                                                 |
| `head_demographics`           | Age, gender, race, education of head   | NIDS individual-derived (joined to `w5_hhid`)                       |

**Not agent fields:** `w5_wgt` (drives the resample), `w5_hhid` (join key).

---

## How the population is built (5 phases)

```
P1 BACKBONE   NIDS → derive income_source, committed/discretionary, savings proxy,
              D_trad, income_quintile   (stays in 2017 Rands — no CPI)
P2 MATCH      FinScope → copy banked / credit / savings / informal flags
              onto each NIDS household, by income-quintile cell (× province if it fits)
P3 RESAMPLE   draw 5,000 households, probability ∝ w5_wgt (with replacement)
P4 VALIDATE   internal NIDS distributions + FinScope-marginal match diagnostics
P5 INSTANTIATE  each row → Household Agent (balance sheet + flags + tags)
                       │
                       ▼
              5,000 Household Agents, ready for the ABM
```

Weighting in P3 makes 5,000 sampled households look like the real national population, at a fixed
size we can re-run many times.

---

## Three honest assumptions (flagged for the chapter)

1. **2017 throughout** — the population reflects 2017 conditions; results are not forwarded to a
   current year. A deliberate scope choice, not an oversight.
2. **FinScope 2019 as a 2017 proxy** — we have no 2017 FinScope wave; the 2-year gap on categorical
   flags is noted, not corrected.
3. **Crude match** — flags are copied at the income-quintile cell level, so they reproduce cell
   marginals but not finer joint structure.

---

## What this agent does *not* have yet (on purpose)

- No BNPL balance — arrives with the BNPL extension.
- No peer/neighbour links — households don't interact in the baseline.
- One simple lender only — no multi-bank competition yet.
- No behavioural validation targets yet — those come from **BNPL providers** later.

---

## See also

- [`OVERVIEW.md`](OVERVIEW.md) — living source of truth (strategy + execution plan).
- [`scratchpad/variables.md`](scratchpad/variables.md) — full column-level variable list.
- [`scratchpad/data_fusion.md`](scratchpad/data_fusion.md) — the simple cell-donor matching method.
- [`scratchpad/decision.md`](scratchpad/decision.md) — why each decision was made.
