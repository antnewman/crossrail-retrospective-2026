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

**Method applied:** Headline direct count comparison. No deflator. Baseline 200,000,000 (2011 business case rounded forecast, "full opening steady state") compared against ORR 2024/25 outturn 242,866,594.

**Observations used:**
- `crossrail_retrospective.assumptions.value = 200,000,000` (passenger_journeys_full_opening, baseline_date 2011-07-01, unit count) [baseline]
- `ORR-EL-JOURNEYS @ 2025-03-31 = 242.866594 million = 242,866,594` (fiscal year April 2024 to March 2025, provisional per ORR, loaded from ORR Table 1223a) [comparison]

**Formula:**
```
drift_absolute = 242,866,594 - 200,000,000 = 42,866,594
drift_percent = drift_absolute / 200,000,000 × 100 = 21.4333%
```

**Decisions made:**

- **Single row, headline drift only.**
  - Alternatives considered: two-component decomposition per caveat 2 (pre-pandemic trend drift vs post-pandemic recovery); defer entire calculation until a London rail proxy is loaded.
  - Decision: single headline row, with caveat 2 decomposition deferred as a follow-up unit.
  - Reasoning: proper caveat 2 decomposition requires a London rail proxy series (e.g. ORR TfL Underground annual journeys, or a comparable TOC journeys series) for 2011-2019 to estimate the no-pandemic counterfactual. No such proxy is loaded. Attempting an ad-hoc decomposition with the GB total series (Table 1220) risks producing a defensible-looking but methodologically weak number. The headline drift is publishable with the decomposition-deferred caveat clearly stated.

- **Unit alignment: store comparison in absolute count, not millions.**
  - Alternatives considered: store in millions to match the ORR series unit; store in absolute count to match the assumption unit.
  - Decision: absolute count.
  - Reasoning: the drift row's `assumption_id` links to an assumption with `unit = count`; readers will naturally read the drift in the assumption's unit. 242.866594 × 1,000,000 = 242,866,594 exactly, so precision is preserved.

- **Date semantics: original dates on the row (no price base here).**
  - Reasoning: no deflator, so no price base question. `baseline_date = 2011-07-01` (assumption) and `comparison_date = 2025-03-31` (observation). Straightforward.

**Caveats applied:**

- Caveat 2 (pandemic as break in demand series): decomposition deferred. Captured as an open question below.
- Ramp-up non-completion (informal caveat not in the formal three): 2024/25 is year three of operation; the 2011 forecast is "at full opening, steady state". 2024/25 demand is still growing per the assumption's own description. The +21.4% headline likely UNDERSTATES the eventual drift between forecast and realised steady-state demand.
- Caveat 3 (multiple restated business cases): acknowledged. No intermediate restated forecast is used.

**Drift result:**

- Residual: +42,866,594 journeys, +21.4333%.
- Direction: positive (outturn exceeds forecast). Robust.
- Magnitude: understates eventual steady-state drift per the ramp-up caveat. The +21.4% is a lower bound on the eventual figure.

**Confidence:** medium. Arithmetic exact. Direction robust. Magnitude directionally understated for the steady-state comparison.

**Notes for methodology.md:**

- Caveat 2 decomposition requires a proxy London rail series that is out of scope for this session. methodology.md should describe the decomposition approach and flag the series dependency.
- Rail demand forecasts at "full opening steady state" are typically compared against ramping-up outturn; methodology.md should describe whether the investigation reports "drift at observation date" (simple, understates for programmes in ramp-up) or "projected drift at steady state" (requires ramp modelling).

**What this tells us about drift patterns more generally:**

Demand forecasts stated "at steady state" can be **over-performed** in the headline comparison yet still **understate** the real drift, if the outturn is measured during an ongoing ramp-up. For long-ramp programmes (rail, power, large-footprint retail), a drift analysis that compares a steady-state forecast against a non-steady-state outturn systematically understates positive drift and may overstate negative drift. The direction of the finding may be robust, but the magnitude is sensitive to ramp-completion timing. This is a distinct axis of methodology risk from the nominal-vs-real framing issue that appears in cost drift.

## Assumption 3: revenue_2024_25

**Method applied:** Deferred this session. No drift row inserted for this assumption.

**Reason for deferral:** TFL-EL-REVENUE has 0 observations in pda_shared.external_observations. The series row exists in pda_shared.external_series but the TfL primary-source values for Elizabeth Line annual passenger income are pending Ant's data supply from TfL Annual Reports and Quarterly Progress Reports (PDFs, not directly parseable without manual extraction).

**Observations used:** none.

**Provisional handling:** no drift row inserted. A rough out-of-session benchmark exists in the London Assembly cross-reference (LONDON-ASSEMBLY-EL-2025, which cites £606m Elizabeth Line passenger income for 2023/24). This figure is for a different fiscal year than the assumption's baseline comparison (2024/25) and is a secondary citation of TfL figures rather than a TfL primary source, so it is noted only as a rough benchmark and not inserted as a drift row. Using it to compute a provisional drift would risk being misread as a TfL-sourced comparison when it is not.

**What unblocks this calculation:** three TfL Annual Report values for Elizabeth Line annual passenger income for fiscal years 2022/23, 2023/24, and 2024/25, with primary TfL citations (document title, section, and date). Once supplied, these values load into TFL-EL-REVENUE via the same ingest pattern used for the other series (YAML provenance file + per-row SQL insert, committed together).

**Follow-up:** separate small session once the three TfL values are supplied. Will produce one drift row (baseline £1.037bn December 2019 TfL Business Plan forecast for 2024/25, comparison 2024/25 TfL outturn). Similar shape to assumption 2 (direct comparison, no deflator required between a 2019 forecast and a 2024/25 outturn at the order-of-magnitude framing; a more rigorous version would deflate both to a common price year, but that is a Path B methodology refinement for later).

**Caveats that will apply when the calculation is run:** Caveat 2 (pandemic break), per assumption description, because the December 2019 forecast was the last pre-pandemic published forecast and the comparison period is entirely post-pandemic.

**Drift result:** pending.

**Confidence:** n/a (no calculation yet).

**Notes for methodology.md:** methodology.md should note explicitly that assumption 3 is a planned drift row pending data supply, not an omission. The London Assembly cross-reference provides a rough directional expectation (2023/24 outturn ~£606m vs forecast ramp ~£884m for 2023/24, suggesting a substantial negative drift). The 2024/25 comparison against the £1.037bn forecast is expected to be similarly negative, but precise figures must come from TfL primary sources.

**What this tells us about drift patterns more generally:**

Assumption 3's deferral is itself a data point about drift methodology: some primary sources (TfL PDFs in this case) are not readily programmatically ingestable without manual extraction, and a disciplined methodology should defer rather than substitute secondary citations. The cost of deferral is a gap in the drift panel; the cost of substitution would be a row that reads as "TfL data" when the provenance is a London Assembly research document. For cumulative cross-investigation comparison work, the distinction between primary and secondary sources must be rigid.

## Assumption 4: benefit_cost_ratio_dft

**Method applied:** Sensitivity-only restatement of the 2011 BCR (1.97, transport-only DfT value) under Scenario A (observed 2024/25 demand and outturn cost). Three co-equal rows reflecting three defensible cost-ratio treatments: nominal cash, real with 7.5% pre-2014 correction, real without pre-2014 correction. Benefits assumed linear in demand. Not a full NPV reconstruction.

**Observations used:**
- `crossrail_retrospective.assumptions.value = 1.97` (benefit_cost_ratio_dft, baseline_date 2011-07-01) [baseline]
- `ORR-EL-JOURNEYS @ 2025-03-31 = 242,866,594` (same demand observation as assumption 2; benefit driver)
- `NAO-CROSSRAIL-2021 outturn = £18,800,000,000` (cost driver, cash terms)
- `ONS-OPI-INFRA-NEW @ 2014-01-31 = 100.2`, `mean of calendar 2017 = 102.025` (deflator inputs for the real cost ratios)
- `crossrail_retrospective.drift_calculations` Row A and Row B of assumption 1 (cost ratios derived from those rows)

**Formula:**
```
demand_ratio           = 242,866,594 / 200,000,000 = 1.21433297
cost_ratio_nominal     = 18,800,000,000 / 14,800,000,000 = 1.27027027
cost_ratio_real_no_corr= 18,463,709,875.03 / 14,800,000,000 = 1.24754796  (from assumption 1 Row A)
cost_ratio_real_with_corr = 18,463,709,875.03 / 15,910,000,000 = 1.16050973  (from assumption 1 Row B)

restated_BCR = 1.97 × demand_ratio / cost_ratio

BCR_nominal        = 1.97 × 1.21433297 / 1.27027027 = 1.883250   (drift -0.086750, -4.4036%)
BCR_real_no_corr   = 1.97 × 1.21433297 / 1.24754796 = 1.917550   (drift -0.052450, -2.6624%)
BCR_real_with_corr = 1.97 × 1.21433297 / 1.16050973 = 2.061367   (drift +0.091367, +4.6379%)
```

**Decisions made:**

- **Three co-equal rows, no primacy.**
  - Alternatives considered: two rows (A-nominal plus a single A-real, with one designated primary); one row (single point estimate with sensitivity range in notes).
  - Decision: three rows, none designated primary.
  - Reasoning: the 7.5% pre-2014 correction used in one of the two real-cost variants is itself an estimate at the middle of a 5-10% plausible range. Labelling the 7.5%-based row as "primary" would claim methodological confidence that the underlying data does not support, and would cascade into findings that overstate the robustness of the band change (see next decision). Matching the neutral A/B pattern of assumption 1 keeps the methodological choice explicit for readers of the findings.

- **Band-change finding is sensitivity-dependent, not robust.**
  - Three rows produce two distinct band outcomes: BCR_nominal (1.883) and BCR_real_no_corr (1.918) both fall in band 2 (medium, 1.5-2.0); BCR_real_with_corr (2.061) falls in band 3 (high, 2.0-4.0).
  - The boundary at which restated BCR crosses 2.0 is a cumulative pre-2014 correction of approximately 4.3%. Below that, band 2; above, band 3.
  - Our stated plausible range for pre-2014 correction is 5-10%, all of which keep BCR just above the 2.0 boundary (BCR 2.01 to 2.11, band 3). But zero correction (Row A-style treatment) gives BCR 1.918 (band 2).
  - The band change is therefore robust within the 5-10% plausible range for pre-2014 inflation, but NOT robust against the question "should any pre-2014 correction be applied at all?". Findings must describe the band change as methodologically sensitive rather than robust.

- **Scenario B (long-run demand trajectory consistent with first three years) deferred.**
  - Reasoning: "plausible trajectory consistent with the first three years" is a judgement call requiring separate framing. Captured as an open question.

- **Confidence: low for all three rows.**
  - Sensitivity-only restatement; benefits assumed linear in demand. Not an NPV reconstruction. Confidence reflects the level of the method, not the arithmetic (which is exact and reproducible).

**Caveats applied:**

- Caveat 1 (ONS-OPI vs BCIS-TPI): applies to the two real-cost rows via the cost ratio; does not apply to the nominal row (no deflator). Magnitude sensitive to index choice.
- Caveat 2 (pandemic break in demand series): applies to all three rows via the demand ratio (same demand observation as assumption 2).
- Caveat 3 (multiple restated business cases): applies. No intermediate restated BCR is compared against.
- Additional for the real-no-correction row: inherits assumption 1 Row A's pre-2014 gap caveat (mixes 2010-11 baseline with Jan-2014 deflated outturn).

**Drift result:**

- Three co-equal rows. Restated BCR range: 1.88 to 2.06.
- Direction: mixed within the range. Nominal and real-no-correction show a small negative drift (BCR slightly below baseline 1.97); real-with-correction shows a small positive drift (BCR slightly above 1.97 and just above the 2.0 band boundary).
- Band result: two of three scenarios stay in band 2 (medium); one moves to band 3 (high). Band change sensitivity-dependent.

**Confidence:** low on all three rows. The arithmetic is exact; the confidence rating reflects the method's level (sensitivity-only order-of-magnitude), not the computation.

**Notes for methodology.md:**

- The three-row structure for assumption 4 mirrors the two-row structure for assumption 1 (which itself reflects the pre-2014 correction choice). methodology.md should describe the cascade: decisions made in the cost deflation step (assumption 1) propagate into the BCR restatement (assumption 4) and into the band result (assumption 5).
- The term "sensitivity-only restatement" means: we re-evaluate the BCR under observed demand and cost ratios, holding the BCR formula's other assumptions constant. This is not a Green Book NPV reconstruction; the confidence rating of "low" is the right level for all three rows.
- The 2.0 band boundary is an externally imposed threshold (DfT TAG VfM framework), not a property of the Crossrail data. Crossing that boundary with a result computed at the tail of the plausible pre-2014 range is a boundary artefact, not a robust finding.

**What this tells us about drift patterns more generally:**

For **categorical findings** (band codes, thresholds, discrete classifications), sensitivity to small methodological choices at the tail of a price-base window can flip the answer. **Continuous metrics (drift percent)** are more robust; **categorical metrics (band crossings)** need explicit sensitivity disclosure. An investigation that reports a band change as a headline should be held to a higher methodological standard than one that reports a continuous percentage drift. For BCR-type analyses specifically, the band framework concentrates methodological risk at each band boundary; a restated BCR within 0.1 of a boundary under one scenario and 0.1 the other side under another is not a robust categorical claim.

## Assumption 5: value_for_money_band

[populated during session]

## Cross-cutting decisions

**Decision:** the method originally specified in INVESTIGATION_BRIEF.md section 6.1 had a methodological flaw (repriced one side of the comparison and not the other). The flaw was caught during implementation of assumption 1 in the first drift calculation session. Corrected method puts both sides in 2010-11 prices using ONS-OPI-INFRA-NEW as the deflator. Affects assumption 1 directly and the inflation treatment in assumption 4 real-cost scenario by implication. INVESTIGATION_BRIEF.md section 6.1 will be updated in a separate commit once the corrected method is finalised.
**Affects assumptions:** 1 (construction_funding_envelope), 4 (benefit_cost_ratio_dft, real-cost scenario by implication).
**Reasoning:** a one-sided reprice (baseline to 2025 prices, outturn in cash) produces a number whose direction depends on the reprice target date rather than on any underlying fiscal fact. The flaw was identified when the pre-execution arithmetic for assumption 1 under the brief-specified method produced a negative residual (apparent real-terms underspend) that would have become a positive residual (apparent real-terms overspend) under a different but equally defensible reprice target date. Both sides must be in the same price base. Expressing both in 2010-11 prices keeps the baseline untouched, deflates the outturn back, and yields a number whose sign is an artefact of the cost data, not the methodology.

## Open questions

**Question:** Caveat 2 (pandemic as break in demand series) decomposition for assumption 2: how should pre-pandemic trend drift (2011 forecast to a counterfactual 2024/25) be separated from post-pandemic recovery drift (2020 to 2025)?
**Arose during:** assumption 2 (passenger_journeys_full_opening).
**Why it matters:** the +21.4% headline drift conflates the two components. A reader wanting to attribute drift causes cannot do so from the headline alone. The decomposition is required by INVESTIGATION_BRIEF.md caveat 2.
**Provisional handling:** no decomposition performed this session; headline drift row written with the deferral and its reasoning recorded in the row's `notes` field. A London rail proxy series (e.g. ORR TfL Underground annual journeys, or a comparable TOC journeys series) for 2011-2019 needs to be loaded first. Follow-up unit of work: load the proxy, compute the 2011-2019 trend, project it to 2024/25 without pandemic, and compare against actual 2024/25 (242.866594m) to decompose drift into trend and recovery components.

**Question:** Scenario B for assumption 4 (BCR restatement): how should the "plausible long-run demand trajectory consistent with the first three years of operation" be defined?
**Arose during:** assumption 4 (benefit_cost_ratio_dft).
**Why it matters:** INVESTIGATION_BRIEF.md section 6.4 specifies two scenarios (A and B) for the BCR restatement. Scenario B requires a demand trajectory projection, which is a judgement call rather than a computation.
**Provisional handling:** deferred this session. Scenario A (three rows, co-equal) written; Scenario B not. Follow-up needs an explicit methodology for "plausible trajectory" (linear extrapolation, exponential decay toward an assumed peak, match to comparable line openings, etc.).

**Question:** At what point is a categorical finding (e.g. band change) strong enough to make a headline claim when the underlying metric sits near a threshold boundary?
**Arose during:** assumption 4, band-boundary sensitivity.
**Why it matters:** Crossrail's restated BCR under one of three co-equal scenarios (real, 7.5% pre-2014 correction) sits at 2.06, just above the 2.0 medium/high boundary. The other two scenarios (BCR 1.88, 1.92) stay below it. A headline reading "Crossrail's VfM band drifted from medium to high" is supported by one of three scenarios but not by the other two; a headline reading "Crossrail's VfM band is on the medium/high boundary with one scenario suggesting a move to high" is more defensible but also less clean.
**Provisional handling:** decisions log records the boundary sensitivity explicitly. Findings must describe the band change as methodologically sensitive rather than robust. A general methodology for headline-strength thresholds near band boundaries is a candidate for the shared methodology-shared.md in the umbrella repo.
