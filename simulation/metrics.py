"""Observation: per-tick metrics and the run summary.

The CCMR band mapping is exact at a 14-day tick, which is the reason k was revised from
6 to 7: 7 ticks is 98 days, inside the 91-120 bucket, so it maps onto the 90+ impairment
convention. k=6 would be 84 days and would land in 61-90 with no clean analogue.

Two counters are tracked separately and must not be conflated:
  * `distress_streak` drives DEFAULT (D7), the model's headline output.
  * `arrears_age_ticks` drives the CCMR BAND comparison (D6).
"""

from __future__ import annotations

import statistics
from collections import Counter
from dataclasses import asdict

from .config import CCMR_BANDS


def ccmr_band(arrears_age_ticks: int) -> str:
    """Map ticks-in-arrears onto the CCMR age-analysis band."""
    for label, lo, hi in CCMR_BANDS:
        if arrears_age_ticks >= lo and (hi is None or arrears_age_ticks <= hi):
            return label
    return "current"  # pragma: no cover


#: The two cumulative CCMR delinquency measures, as the bands each one sums.
BANDS_60_PLUS = ("d61_90", "d91_120", "d120_plus")
BANDS_90_PLUS = ("d91_120", "d120_plus")


def band_share(bands: Counter, labels: tuple[str, ...], denom: int) -> float:
    """Share of `denom` households sitting in `labels`; zero when `denom` is empty."""
    return sum(bands[label] for label in labels) / denom if denom else 0.0


def collect_tick(model) -> dict:
    """One row of per-tick observation."""
    agents = list(model.agents)
    n = len(agents)

    bands = Counter(ccmr_band(a.arrears_age_ticks) for a in agents)
    n_defaulted = sum(1 for a in agents if a.defaulted)
    n_zero_savings = sum(1 for a in agents if a.savings <= 0)

    # The CCMR denominator is ACCOUNTS, held by credit-active consumers. Slightly over
    # half this population holds no traditional debt at all and so can never be in
    # arrears; including them guarantees the model undershoots the target for a reason
    # that has nothing to do with behaviour. The credit-active denominator is the closer
    # analogue and is reported alongside the all-household figure, never instead of it.
    active = [a for a in agents if a.d_trad > 0 or a.arrears_trad > 0]
    n_active = len(active)
    bands_active = Counter(ccmr_band(a.arrears_age_ticks) for a in active)

    bnpl_holders = 0
    stacking = Counter()
    total_bnpl = 0.0
    if model.params.bnpl_enabled:
        for a in agents:
            outstanding = a.bnpl_outstanding()
            total_bnpl += outstanding
            depth = a.stacking_depth()
            stacking[depth] += 1
            if outstanding > 0:
                bnpl_holders += 1
                model.ever_holders.add(a.agent_id)
            if depth >= 2:
                model.ever_stacked.add(a.agent_id)

    row = {
        "tick": model.tick,
        "n_agents": n,
        # --- headline outputs ---------------------------------------------------
        "default_rate": n_defaulted / n,
        "n_defaulted": n_defaulted,
        # --- CCMR bands (D6) ------------------------------------------------------
        **{f"band_{label}": band_share(bands, (label,), n) for label, _, _ in CCMR_BANDS},
        "pct_60_plus": band_share(bands, BANDS_60_PLUS, n),
        "pct_90_plus": band_share(bands, BANDS_90_PLUS, n),
        # --- same bands on the credit-active denominator (the CCMR analogue) --------
        "n_credit_active": n_active,
        **{
            f"active_{label}": band_share(bands_active, (label,), n_active)
            for label, _, _ in CCMR_BANDS
        },
        "active_60_plus": band_share(bands_active, BANDS_60_PLUS, n_active),
        "active_90_plus": band_share(bands_active, BANDS_90_PLUS, n_active),
        # --- traditional stress: the pattern-1 falsification test (D5) ------------
        "trad_debt_total": sum(a.d_trad for a in agents),
        "trad_arrears_total": sum(a.arrears_trad for a in agents),
        "trad_interest_tick": sum(a.interest_charged_tick for a in agents),
        "trad_arrears_rate": sum(1 for a in agents if a.arrears_trad > 0) / n,
        # --- BNPL ------------------------------------------------------------------
        "bnpl_outstanding_total": total_bnpl,
        "bnpl_adoption_rate": bnpl_holders / n,
        "bnpl_volume_tick": sum(a.bnpl_volume_tick for a in agents),
        "bnpl_fees_tick": sum(a.bnpl_fees_tick for a in agents),
        "stacking_mean": (
            sum(d * c for d, c in stacking.items()) / n if stacking else 0.0
        ),
        "stacking_2plus": sum(c for d, c in stacking.items() if d >= 2) / n,
        # --- D17 peer channel diagnostics ------------------------------------------
        # `s_g` is now normalised onto the eligible subpopulation, so it can reach 1.0
        # and a Granovetter threshold drawn on [0,1] is meaningful everywhere. Tracking
        # the peak matters: if the signal never approaches the threshold distribution,
        # a null result in the threshold arm is mechanical rather than substantive.
        "peer_share_mean": (
            sum(model.group_share_lagged.values()) / len(model.group_share_lagged)
            if model.group_share_lagged
            else 0.0
        ),
        "peer_share_max": max(model.group_share_lagged.values(), default=0.0),
        # Share of ELIGIBLE households whose personal threshold has been crossed. This
        # is the adoption-tipping quantity RQ2 needs to separate from default.
        "threshold_triggered": (
            sum(
                1
                for a in agents
                if a.bnpl_eligible
                and model.group_share_lagged.get(a.reference_group, 0.0) >= a.theta
            )
            / max(model.n_bnpl_eligible, 1)
            if model.params.peer_mechanism == "threshold"
            else 0.0
        ),
        # --- pattern 4 (TransUnion 36%) ------------------------------------------
        "zero_savings_rate": n_zero_savings / n,
        # --- D1 diagnostic ----------------------------------------------------------
        "shocked_rate": sum(1 for a in agents if a.shocked_tick) / n,
    }
    return row


def summarise_run(model) -> dict:
    """Collapse a run to one row, discarding burn-in."""
    p = model.params
    post = [r for r in model.history if r["tick"] >= p.burn_in]
    if not post:  # pragma: no cover
        post = model.history
    final = model.history[-1]
    agents = list(model.agents)

    def mean(key: str) -> float:
        return statistics.fmean(r[key] for r in post)

    # --- pattern 3 (Hamill et al.): non-monotonic DTI with a middle-income peak ---
    #
    # PRE-REGISTERED PRIMARY STATISTIC: the AGGREGATE ratio, total debt over total income
    # within each quintile. Chosen on its own merits before checking whether it passes:
    # it is the standard financial-stability measure, it is the form the CCMR reports in,
    # and unlike a mean of ratios it cannot be driven by near-zero denominators.
    #
    # The mean and median of household-level ratios are reported ALONGSIDE it, never
    # instead of it, because the verdict on pattern 3 is statistic-dependent and that
    # dependence is itself a finding. Measured: the mean is carried almost entirely by a
    # handful of Q1 households (top 1% of Q1 hold 77% of its DTI mass, median Q1 = 0.00),
    # so a mean of ratios is not a meaningful measure over this population.
    #
    # All households are retained, including the zero-capacity debtors. Excluding them
    # would flip the verdict, which is exactly why they stay: P2's decision was to report
    # them as a finding, and dropping data to make a test pass is the circularity this
    # project has avoided elsewhere.
    dti_aggregate: dict[str, float] = {}
    dti_mean: dict[str, float] = {}
    dti_median: dict[str, float] = {}
    for q in ("Q1", "Q2", "Q3", "Q4", "Q5"):
        members = [a for a in agents if a.rec.income_quintile == q]
        if not members:
            continue
        total_income = sum(a.income_monthly for a in members)
        dti_aggregate[q] = (
            sum(a.total_debt() for a in members) / total_income if total_income > 0 else 0.0
        )
        ratios = [
            a.total_debt() / a.income_monthly if a.income_monthly > 0 else 0.0
            for a in members
        ]
        dti_mean[q] = statistics.fmean(ratios)
        # Median over DEBTORS. Over all households it is identically zero in every
        # quintile, since fewer than half hold any debt, which makes it uninformative.
        debtor_ratios = [
            a.total_debt() / a.income_monthly
            for a in members
            if a.total_debt() > 0 and a.income_monthly > 0
        ]
        dti_median[q] = statistics.median(debtor_ratios) if debtor_ratios else 0.0

    # --- D11 binding checks -------------------------------------------------------
    n_requests = sum(pl.n_requests for pl in model.platforms)
    n_order_cap = sum(pl.n_blocked_order_cap for pl in model.platforms)
    n_rolling = sum(pl.n_blocked_rolling_limit for pl in model.platforms)

    # The rolling limit now scales with household income, so it binds hardest at the
    # bottom. An aggregate binding rate can read as inert while the constraint is biting
    # hard on Q1, which is exactly the failure the flat constant hid.
    quintile_of = {a.agent_id: a.rec.income_quintile for a in agents}
    req_q: Counter[str] = Counter()
    blk_q: Counter[str] = Counter()
    for pl in model.platforms:
        for agent_id, count in pl.requests_by_agent.items():
            req_q[quintile_of[agent_id]] += count
        for agent_id, count in pl.blocked_rolling_by_agent.items():
            blk_q[quintile_of[agent_id]] += count

    # --- D4 purchase-size validation ------------------------------------------------
    # Checked against the SA provider disclosure (bnpl_anchors_2017.json), never fitted
    # to it. The rule's scale comes from the IES budget share.
    realised_purchase_mean = (
        model.want_purchase_value / model.want_purchase_count
        if model.want_purchase_count
        else 0.0
    )

    summary = {
        # Every parameter is echoed, so a run is identifiable from its own row and not
        # only from its label. `n_agents` is echoed as requested (None = full population)
        # and then overwritten below by the realised count, which is the one to report.
        **asdict(p),
        # --- headline -----------------------------------------------------------
        "default_rate_final": final["default_rate"],
        "default_rate_mean": mean("default_rate"),
        "pct_90_plus_final": final["pct_90_plus"],
        "pct_90_plus_mean": mean("pct_90_plus"),
        "pct_60_plus_final": final["pct_60_plus"],
        "pct_60_plus_mean": mean("pct_60_plus"),
        "pct_current_final": final["band_current"],
        "pct_current_mean": mean("band_current"),
        # --- the CCMR comparison, on the credit-active denominator -----------------
        "active_90_plus_final": final["active_90_plus"],
        "active_90_plus_mean": mean("active_90_plus"),
        "active_60_plus_final": final["active_60_plus"],
        "active_60_plus_mean": mean("active_60_plus"),
        "active_current_final": final["active_current"],
        **{f"active_{label}_mean": mean(f"active_{label}") for label, _, _ in CCMR_BANDS},
        "n_credit_active_final": final["n_credit_active"],
        # --- pattern 1: traditional stress --------------------------------------
        "trad_arrears_rate_mean": mean("trad_arrears_rate"),
        "trad_interest_total": sum(r["trad_interest_tick"] for r in post),
        "trad_debt_final": final["trad_debt_total"],
        # --- pattern 4 ------------------------------------------------------------
        "zero_savings_rate_mean": mean("zero_savings_rate"),
        # --- BNPL / RQ2 / RQ3 -----------------------------------------------------
        "bnpl_adoption_final": final["bnpl_adoption_rate"],
        "bnpl_volume_cumulative": sum(r["bnpl_volume_tick"] for r in post),
        "bnpl_fees_cumulative": sum(r["bnpl_fees_tick"] for r in post),
        "bnpl_outstanding_final": final["bnpl_outstanding_total"],
        "stacking_mean_final": final["stacking_mean"],
        "stacking_2plus_final": final["stacking_2plus"],
        # --- D17 peer channel: the adoption-vs-default separation (RQ2) -------------
        "peer_share_mean_final": final["peer_share_mean"],
        "peer_share_max_final": final["peer_share_max"],
        "peer_share_max_ever": max(r["peer_share_max"] for r in post),
        "threshold_triggered_final": final["threshold_triggered"],
        "threshold_triggered_mean": mean("threshold_triggered"),
        # --- D1 diagnostic --------------------------------------------------------
        "shocked_rate_mean": mean("shocked_rate"),
        # --- population / eligibility --------------------------------------------
        "n_agents": final["n_agents"],
        "n_banked": model.n_banked,
        "n_bnpl_eligible": model.n_bnpl_eligible,
        "n_zero_capacity_debtors": len(model.zero_capacity_debtors),
        # --- D11 binding checks ---------------------------------------------------
        "bnpl_requests": n_requests,
        "bnpl_order_cap_bind_rate": (n_order_cap / n_requests) if n_requests else 0.0,
        "bnpl_rolling_limit_bind_rate": (n_rolling / n_requests) if n_requests else 0.0,
        # --- D4 purchase-size validation ------------------------------------------
        "bnpl_want_purchases": model.want_purchase_count,
        "bnpl_purchase_mean_realised": realised_purchase_mean,
        # --- lender ----------------------------------------------------------------
        "trad_applications": model.lender.n_applications,
        "trad_granted": model.lender.n_granted,
        "trad_granted_value": model.lender.value_granted,
        "trad_refused_gate": model.lender.n_refused_gate,
    }
    quintiles = sorted(set(quintile_of.values()))
    summary.update(
        {
            f"bnpl_rolling_bind_{q}": blk_q[q] / req_q[q] if req_q[q] else 0.0
            for q in quintiles
        }
    )
    # D4 purchase check by quintile: who buys, and at what size (DEFECTS.md B32).
    for q in quintiles:
        n_q = model.want_purchase_count_q[q]
        summary[f"bnpl_want_purchases_{q}"] = n_q
        summary[f"bnpl_purchase_mean_realised_{q}"] = (
            model.want_purchase_value_q[q] / n_q if n_q else 0.0
        )
    # `dti_` is the PRIMARY (aggregate) statistic; the others are the secondary readings.
    summary.update({f"dti_{q}": v for q, v in dti_aggregate.items()})
    summary.update({f"dti_mean_{q}": v for q, v in dti_mean.items()})
    summary.update({f"dti_median_{q}": v for q, v in dti_median.items()})
    # --- by quintile, and over the horizon ------------------------------------------
    # The introduction promises default by income quintile; the CFPB stacking figure is
    # over a period, so the point-in-time 2+ share needs a horizon analogue.
    n = len(agents)
    for q in quintiles:
        members = [a for a in agents if a.rec.income_quintile == q]
        n_q = len(members)
        summary[f"n_agents_{q}"] = n_q
        summary[f"default_rate_final_{q}"] = (
            sum(1 for a in members if a.defaulted) / n_q if n_q else 0.0
        )
        summary[f"bnpl_adoption_final_{q}"] = (
            sum(1 for a in members if a.bnpl_outstanding() > 0) / n_q if n_q else 0.0
        )
        summary[f"trad_arrears_final_{q}"] = (
            sum(1 for a in members if a.arrears_trad > 0) / n_q if n_q else 0.0
        )
    summary["ever_adopted"] = len(model.ever_holders) / n
    summary["ever_stacked_2plus"] = len(model.ever_stacked) / n
    summary["ever_stacked_2plus_of_adopters"] = (
        len(model.ever_stacked) / len(model.ever_holders) if model.ever_holders else 0.0
    )
    return summary
