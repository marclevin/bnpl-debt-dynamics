"""Generate the Appendix B parameter register from the code's own declarations.

Writes thesis/chapters/appendix_b_register.tex. Parameter names, rules, provenance and values
are read from simulation.config and simulation.experiments, so the table cannot drift from
the code. The wording of the Source and Sweep columns is thesis text and lives in REGISTER
below; the script fails if a parameter is declared in the code and missing here, or the
reverse. Re-run after any change to simulation/config.py:

    PYTHONPATH=. .venv/bin/python notebooks/scripts/generate_param_register.py
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from simulation.config import parameter_register  # noqa: E402
from simulation.experiments import calibrated  # noqa: E402

OUT = ROOT / "thesis" / "chapters" / "appendix_b_register.tex"

PROVENANCE_LABELS = {
    "SOURCED": "sourced",
    "DERIVED": "derived",
    "ASSUMPTION": "assumed",
    "FITTED": "fitted",
}

#: The design record numbers its decisions D1 to D17; Table submodels numbers the submodels.
#: The two orders differ from D11 on, so the register prints the submodel.
SUBMODEL = {
    "D1": "1", "D2": "2", "D3": "3", "D4": "4", "D5": "5", "D6": "6", "D7": "7", "D9": "9",
    "D10": "10", "D11": "12", "D12": "13", "D13": "14", "D14": "15", "D16": "17", "D17": "11",
    "ODD": "design", "OVERVIEW 1a": "design", "P3": "data",
}

#: parameter -> (source, sweep). LaTeX, printed as written.
REGISTER: dict[str, tuple[str, str]] = {
    "n_ticks": (r"A 24-month horizon at a 14-day tick (Section~\ref{sec:sim-params}).", ""),
    "burn_in": (r"The first 12 ticks are excluded from post-burn-in summaries (Section~\ref{sec:sim-params}).", ""),
    "n_agents": (r"The full resampled population of 5{,}000 (Appendix~\ref{app:variables}, Part~D.10).",
                 r"1{,}000 / 5{,}000 / 10{,}000"),
    "shock_prob": (r"Fitted to the \ac{CCMR} 90+ day band. Reported against the \ac{QLFS} 2017 job-separation band of 0.54\%--1.17\% per tick, to which it is not fitted.",
                   r"calibration grid; 0.005--0.026 in the Sobol design"),
    "shock_persistent": (r"An unemployment spell lasts until re-employment. In the \ac{QLFS} 2017, 68.4\% of the unemployed were still unemployed a quarter later.",
                         r"single-tick shock as a robustness arm"),
    "shock_exit_prob": (r"Re-employment hazard per tick. In the \ac{QLFS} 2017, 11.6\% of the unemployed moved into employment in a quarter, which is 1.87\% per tick.", ""),
    "discretionary_floor": (r"Discretionary spending can be compressed to zero.", ""),
    "q_base": (r"Probability of a want-driven purchase in a tick without peer influence. No source.",
               r"0.01--0.30 in the Sobol design"),
    "beta": (r"Strength of peer influence under the linear rule (Equation~\ref{eq:peer}). No source. $\beta = 0$ is the control.",
             r"0 / 0.5 / 1 / 2 / 3 in the platform and access experiments; 0 and 1 elsewhere"),
    "peer_mechanism": (r"The rule by which adoption spreads: linear (Equation~\ref{eq:peer}) or heterogeneous thresholds \cite{granovetter1978threshold}.",
                       r"both rules on the same access grid"),
    "mu_theta": (r"Mean adoption threshold: the share of a household's reference group that must hold \ac{BNPL} before the household responds. No source.",
                 r"0.15 / 0.30 / 0.45 at full access"),
    "sigma_theta": (r"Dispersion of adoption thresholds, truncated to $[0,1]$. No source. Granovetter's argument concerns the dispersion of thresholds, so this is the axis swept.",
                    r"0.05--0.40"),
    "gamma": (r"Rise in the purchase probability once a household's threshold is crossed. No source. $\gamma = 0$ is the control.",
              r"0 and 0.3"),
    "amount_rule": (r"No estimate was located of what households borrow against a shortfall.",
                    r"exact shortfall / $+25\%$ / plus one tick of committed expenditure"),
    "shortfall_checkout_financed": (r"Whether the household can borrow from the traditional lender the quarter of a shortfall agreement that is paid at checkout. No source says which holds.",
                                    r"on / off (Table~\ref{tab:effect})"),
    "shortfall_bnpl_capped": (r"Limits the \ac{BNPL} share of a shortfall request to $\kappa$ times the household's monthly discretionary budget, the quantity that sizes a want-driven purchase.",
                              r"capped / uncapped, crossed with the three amount rules"),
    "bnpl_purchase_base": (r"The budget against which a purchase is sized. \ac{BNPL} finances discretionary consumption, so the reference is the household's discretionary budget.",
                           r"discretionary / income"),
    "bnpl_purchase_ratio": (r"$\kappa$: the share of discretionary spending in the categories that \ac{BNPL} finances, derived from \ac{IES} 2022/23 microdata \cite{statssa_ies_2023}.",
                            r"0.07--0.28, half to twice the derived share"),
    "bnpl_purchase_cv": (r"Dispersion of purchase size around its mean, which is lognormal. No source.", ""),
    "min_payer_share": (r"29\% of United States card accounts pay at or near the minimum \cite{Keys2019}.",
                        r"0.20--0.40"),
    "payment_friction": (r"Probability per tick of missing a traditional instalment that the household could pay \cite{Kuchler2021}. Fitted to the \ac{CCMR} 1--30 day band.",
                         r"calibration grid"),
    "min_payment_frac": (r"Minimum payment as a share of the balance per month. The \ac{NCA} prescribes no formula.",
                         r"0.025--0.10"),
    "k_default": (r"Seven ticks are 98 days, the first tick boundary past the 90-day impairment convention.",
                  r"four ticks (56 days)"),
    "bnpl_bureau_visible": (r"\ac{BNPL} is not reported to the bureau in the benchmark \cite{nortonrose_bnpl_sa, transunion_cps_sa_2025}.",
                            r"on / off (Section~\ref{sec:scenarios})"),
    "bnpl_enabled": (r"The 2017 baseline has no \ac{BNPL}; the experiments enable it.", r"on / off"),
    "bnpl_access_rate": (r"Share of banked households that are eligible for \ac{BNPL}. Banked households are 82.8\% of the population.",
                         r"0--1.0 in seven steps"),
    "n_platforms": (r"PayJustNow, Payflex, Mobicred and TymeBank were active in South Africa.", r"1--6"),
    "bnpl_order_cap": (r"A per-order cap of R15{,}000 at 2026 vintage, deflated to 2017 Rands.", ""),
    "bnpl_limit_income_multiple": (r"$\lambda$: the limit per platform as a multiple of monthly income. No South African provider publishes a limit; the value is set against Woolard's illustrative stacked exposure \cite{woolard2021}.",
                                   r"0.10--1.0"),
    "bnpl_instalments": (r"Pay-in-four: a quarter at checkout and a quarter at each of the next three ticks \cite{payflex_terms}.", ""),
    "bnpl_late_fee_per_tick": (r"A late fee of R95 a week, R190 a tick, at 2026 vintage \cite{payflex_terms}, deflated to 2017 Rands.", ""),
    "bnpl_late_fee_cap": (r"Late fees on an agreement are capped at R285 over its life, at 2026 vintage \cite{payflex_terms}, deflated to 2017 Rands.", ""),
    "bnpl_late_fee_cap_share": (r"Late fees on an agreement are capped at the lower of the Rand cap and half the purchase price \cite{payflex_terms}.", ""),
    "bnpl_affordability_check": (r"Applies the Regulation 23A test to each \ac{BNPL} request, the analogue of the \ac{FCA}'s affordability check \cite{fca_ps26_1}.",
                                 r"on / off (Section~\ref{sec:scenarios})"),
    "k_cool": (r"Ticks for which want-driven purchases are blocked after a want-driven purchase. One tick is the fourteen-day right of withdrawal in the United Kingdom's rules \cite{fca_ps26_1}.",
               r"0--4 ticks (Appendix~\ref{app:levers})"),
    "stacking_cap": (r"Cap on platforms owed: a household that owes this many platforms or more is refused every new agreement. Hypothetical; no jurisdiction imposes one.",
                     r"1--3 (Appendix~\ref{app:levers})"),
    "activation": (r"Random order, redrawn every tick \cite{comer2013activation, alizadeh2015activation}.",
                   r"fixed order as a robustness arm"),
}


def escape_param(name: str) -> str:
    """Parameter names are typewriter and unbreakable; allow breaks at underscores."""
    return name.replace("_", r"\_\allowbreak{}")


def fmt_rule(rule: str) -> str:
    return "/".join(SUBMODEL[r] for r in rule.split("/"))


def fmt_value(name: str, value: object) -> str:
    if name == "n_agents" and value is None:
        return "5{,}000"
    if value is None:
        return "none"
    if isinstance(value, bool):
        return "on" if value else "off"
    if isinstance(value, float):
        return f"{value:,.6g}".replace(",", "{,}")
    return str(value).replace("_", r"\_")


def main() -> None:
    rows = parameter_register()
    declared = [r["parameter"] for r in rows]
    missing = [n for n in declared if n not in REGISTER]
    extra = [n for n in REGISTER if n not in declared]
    assert not missing and not extra, f"REGISTER out of step with config.py: missing {missing}, extra {extra}"
    reference = calibrated()

    head = r"\textbf{Parameter} & \textbf{Submodel} & \textbf{Value} & \textbf{Prov.} & \textbf{Source} & \textbf{Sweep} \\"
    lines = [
        "% GENERATED by notebooks/scripts/generate_param_register.py from",
        "% simulation/config.py -- do not edit by hand; re-run the script instead.",
        r"\begingroup",
        r"\setlength{\tabcolsep}{3pt}",
        r"\newcolumntype{R}[1]{>{\scriptsize\raggedright\arraybackslash}p{#1}}",
        r"\begin{longtable}{R{2.4cm}R{1.5cm}R{1.75cm}R{1.15cm}R{3.5cm}R{2.85cm}}",
        r"\caption{The full parameter register}",
        r"\label{tab:param-register} \\",
        r"\multicolumn{6}{p{13.4cm}}{\footnotesize Every model parameter. Names, submodels,",
        r"provenance and values are read from the parameter declarations in the code, so the",
        r"table and the code cannot drift apart. Columns: the parameter name in the code; the",
        r"submodel of Table~\ref{tab:submodels} that it belongs to (``design'' marks the",
        r"experimental design and ``data'' the data layer); its value in the benchmark",
        r"configuration, with both fitted parameters at their fitted values; its provenance; the",
        r"source that fixes or motivates the value; and the range swept where one applies.",
        r"Provenance: sourced = a citation fixes the value; derived = the value is computed from",
        r"data; fitted = the value is chosen by calibration; assumed = no anchor exists. Rand",
        r"values are 2017 Rands; the \ac{BNPL} contract parameters are published at 2026 vintage",
        r"and deflated once (Appendix~\ref{app:variables}, Part~D.12).} \\",
        r"\toprule",
        head,
        r"\midrule",
        r"\endfirsthead",
        r"\toprule",
        head,
        r"\midrule",
        r"\endhead",
        r"\bottomrule",
        r"\endfoot",
    ]
    for row in rows:
        name = row["parameter"]
        source, sweep = REGISTER[name]
        cells = [
            r"\texttt{" + escape_param(name) + "}",
            fmt_rule(row["rule"]),
            fmt_value(name, getattr(reference, name)),
            PROVENANCE_LABELS[row["provenance"]],
            source,
            sweep or "--",
        ]
        lines.append(" & ".join(cells) + r" \\")
        lines.append(r"\addlinespace")
    if lines[-1] == r"\addlinespace":
        lines.pop()
    lines += [r"\end{longtable}", r"\endgroup", ""]

    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)} ({len(rows)} parameters)")


if __name__ == "__main__":
    main()
