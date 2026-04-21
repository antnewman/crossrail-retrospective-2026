# Drift calculations: decisions log

Session date: 2026-04-21
Session purpose: capture methodological decisions made during Crossrail drift calculations, for use in writing methodology.md.

This log is updated in real time during the drift calculations session. Each entry records a decision, the alternatives considered, and the reasoning for the choice made.

## Assumption 1: construction_funding_envelope

**Method applied:** Corrected two-sided deflation (per cross-cutting decision above). The £18.8bn cash outturn is deflated to January 2014 prices using ONS-OPI-INFRA-NEW, with calendar-2017 mean-of-twelve monthly index values as the proxy spend-weighted midpoint of the programme. The £14.8bn baseline is compared in the same price base, first unadjusted (Row A) and then with a 7.5% cumulative pre-2014 construction-inflation roll-forward from 2010-11 to January 2014 prices (Row B).

**Observations used:**
- `crossrail_retrospective.assumptions.value = 14,800,000,000` (£, 2010-11 prices, assumption_key construction_funding_envelope, baseline_date 2011-07-01) [baseline]
- `ONS-OPI-INFRA-NEW @ 2014-01-31 = 100.2` [price base anchor]
- `ONS-OPI-INFRA-NEW @ 2017-01 to 2017-12 = 101.2, 101.2, 100.8, 100.8, 101.7, 101.7, 102.3, 102.6, 102.9, 102.8, 103.0, 103.3; mean = 102.025 exactly` [proxy spend-weighted midpoint]
- `NAO-CROSSRAIL-2021 outturn = £18,800,000,000 cash (funding package agreed December 2020)` [comparison, not a loaded observation; stored as an inline figure in the drift row with citation]

**Formula:**
```
deflator             = ONS-OPI-INFRA-NEW[2014-01-31] / mean(ONS-OPI-INFRA-NEW 2017 monthly)
                     = 100.2 / 102.025 = 0.982112...
deflated_outturn     = 18,800,000,000 × deflator = 18,463,709,875.03  (Jan 2014 prices)

Row A (unadjusted):
  residual           = deflated_outturn - 14,800,000,000
                     = 3,663,709,875.03
  drift_percent      = residual / 14,800,000,000 × 100 = 24.7548%

Row B (pre-2014 correction 7.5% cumulative):
  adjusted_baseline  = 14,800,000,000 × 1.075 = 15,910,000,000  (Jan 2014 prices)
  residual           = deflated_outturn - adjusted_baseline = 2,553,709,875.03
  drift_percent      = residual / 15,910,000,000 × 100 = 16.0510%
```

**Decisions made:**

- **Corrected deflation method** (cross-reference: Cross-cutting decisions entry above). Original brief method was one-sided; corrected method puts both sides in same price base.
  - Alternatives considered: Option 1 (year-by-year spend profile from NAO 2019/2021), Option 2 (single proxy-year deflate).
  - Decision: Option 2.
  - Reasoning: time cost vs payoff. Option 1 requires fetching and parsing NAO PDFs that we have not loaded, and NAO reports do not reliably present clean annual spend tables for the full programme life. The precision gain from a year-by-year deflate is likely within the other uncertainty bounds (index choice per caveat 1, pre-2014 gap). Option 2 is simpler, fully reproducible from loaded ONS data, and consistent with the investigation's Path B order-of-magnitude framing.

- **Proxy year = calendar 2017, mean of twelve monthly ONS-OPI-INFRA-NEW values = 102.025.**
  - Alternatives considered: single-month 2016, 2017, or 2018 values; a 2015-2018 mean; a 2016-2017 mean.
  - Decision: calendar 2017 mean (single year, 12-month mean).
  - Reasoning: construction peak spend concentrated 2014-2019 per NAO reporting cadence; 2017 is a defensible rough midpoint. Twelve-month mean reduces sensitivity to the particular month chosen. The index is close to the 2014-2018 rolling mean (102.85) so the choice is robust against small year-shifts.

- **Two rows (A + B) rather than one.**
  - Alternatives considered: one row either with or without pre-2014 adjustment; one row with both results in notes.
  - Decision: two rows, clearly distinguished in notes.
  - Reasoning: the pre-2014 adjustment is itself a decision with a bounded range; publishing both lets a reader compare and pick. Captures the residual as a range (£2.5-3.7bn) rather than a point estimate.

- **7.5% cumulative pre-2014 adjustment (Row B).**
  - Alternatives considered: 5%, 7.5%, 10% cumulative; load BIS OPI linked historical series to derive precisely.
  - Decision: 7.5% cumulative, at the middle of a 5-10% plausible range.
  - Reasoning: 7.5% over ~2.5 years is ~2.9% annual compound, consistent with BIS Construction Output Price Index Infrastructure new work for 2011-2014 per publicly documented construction inflation of the period. BIS OPI linked series not loaded (out of scope for this session). Justification captured in Row B's notes field.

- **Date semantics on the drift row.**
  - Alternatives considered: original dates (2011-07-01 for baseline, 2020-12-31 for outturn); price-base date (2014-01-31 both).
  - Decision: price-base date on both `baseline_date` and `comparison_date`.
  - Reasoning: baseline and comparison are both stored in Jan 2014 prices after the deflator. Using 2014-01-31 on the row makes the price base of the stored values explicit; original dates captured in notes.

**Caveats applied:**

- Caveat 1 (ONS-OPI-INFRA-NEW vs BCIS-TPI): the magnitude is not robust to the index choice. The direction is robust under the corrected method (unlike under the original one-sided reprice).
- Caveat 3 (comparison is 2011 baseline vs 2020-settled outturn, not against any intermediate restated BCR).

**Drift result:**

- Row A (unadjusted): residual +£3.66bn, +24.75% real-terms overspend vs Jan 2014-priced baseline.
- Row B (7.5% pre-2014 correction): residual +£2.55bn, +16.05% real-terms overspend vs Jan 2014-priced adjusted baseline.
- **Reporting range: residual approximately £2.5-3.7bn, approximately 15-25% real-terms overspend.**
- Direction: positive (real-terms overspend). Robust under the corrected method.

**Confidence:** medium. Arithmetic is exact and reproducible. Direction of finding is robust under the corrected method. Magnitude depends on (a) proxy-year choice; (b) pre-2014 gap treatment (Row B estimate vs loading BIS series); (c) ONS-OPI vs BCIS-TPI choice per caveat 1.

**Notes for methodology.md:**

- Reprice target date / price base choice is a first-order methodological decision, not a detail. The original brief's "reprice baseline to current" specification was flawed because it produced a direction-sensitive result. methodology.md section 6.1 must specify "both sides in the same price base via deflating the outturn" rather than "repricing the baseline to current prices".
- The proxy-year choice (single-year vs year-by-year) is order-of-magnitude appropriate at this stage. Flag as a potential refinement target if a finding is sensitive to it.
- The pre-2014 gap is a real publication gap in the ONS OPI series (2014-01 base year for the current publication) and must be disclosed whenever a pre-2014 baseline is being compared. Row B's 7.5% estimate approach is a simple public-knowledge estimate; a more defensible future approach is to load the BIS linked historical series.

**What this tells us about drift patterns more generally:**

Cash overrun headlines (here +28% vs the 2010 budget, the PAC framing) conflate construction price inflation with real-terms cost growth. For major UK infrastructure programmes spanning a decade or more, nominal cash figures systematically overstate real-terms drift; the gap between nominal and real is quantified by construction-sector inflation over the programme's life. In Crossrail's case this is approximately a 25-point gap (28% nominal vs approximately 15-25% real). Drift analyses that report only cash overrun therefore overstate performance deviation, particularly for programmes running through high-inflation periods. Nominal-vs-real framing is a first-order choice in any drift analysis of a multi-year programme.

## Assumption 2: passenger_journeys_full_opening

[populated during session]

## Assumption 3: revenue_2024_25

[populated during session]

## Assumption 4: benefit_cost_ratio_dft

[populated during session]

## Assumption 5: value_for_money_band

[populated during session]

## Cross-cutting decisions

**Decision:** the method originally specified in INVESTIGATION_BRIEF.md section 6.1 had a methodological flaw (repriced one side of the comparison and not the other). The flaw was caught during implementation of assumption 1 in the first drift calculation session. Corrected method puts both sides in 2010-11 prices using ONS-OPI-INFRA-NEW as the deflator. Affects assumption 1 directly and the inflation treatment in assumption 4 real-cost scenario by implication. INVESTIGATION_BRIEF.md section 6.1 will be updated in a separate commit once the corrected method is finalised.
**Affects assumptions:** 1 (construction_funding_envelope), 4 (benefit_cost_ratio_dft, real-cost scenario by implication).
**Reasoning:** a one-sided reprice (baseline to 2025 prices, outturn in cash) produces a number whose direction depends on the reprice target date rather than on any underlying fiscal fact. The flaw was identified when the pre-execution arithmetic for assumption 1 under the brief-specified method produced a negative residual (apparent real-terms underspend) that would have become a positive residual (apparent real-terms overspend) under a different but equally defensible reprice target date. Both sides must be in the same price base. Expressing both in 2010-11 prices keeps the baseline untouched, deflates the outturn back, and yields a number whose sign is an artefact of the cost data, not the methodology.

## Open questions

[methodological questions surfaced during the session but not resolved]
