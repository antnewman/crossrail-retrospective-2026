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

Originally deferred in the first drift calculations session (see earlier entry in git history on branch `analysis/drift-calculations`). Ant Newman supplied three TfL primary-source values in a subsequent session; TFL-EL-REVENUE observations were loaded, and the drift calculation was performed on branch `analysis/drift-revenue`. This entry supersedes the deferral record.

**Method applied:** Direct comparison of the 2019 TfL Business Plan forecast of £1,037m for Elizabeth line passenger income in 2024/25 against the 2024/25 outturn reported in TfL Quarterly Performance Report Q4 2024/25. No deflator applied. Single drift row. Yield decomposition computed as supporting analysis in the row's notes field, not as a separate row.

**Observations used:**
- `crossrail_retrospective.assumptions.value = 1,037,000,000` (revenue_2024_25, baseline_date 2019-12-17, unit gbp) [baseline]
- `TFL-EL-REVENUE @ 2025-03-31 = 652 gbp_millions = 652,000,000 gbp` (fiscal year April 2024 to March 2025; TfL QPR Q4 2024/25 PUB25_029, Elizabeth line financial summary p.13) [comparison]
- For yield decomposition in notes: `ORR-EL-JOURNEYS @ 2025-03-31 = 242,866,594` (actual 2024/25 demand); `2019 TfL Business Plan forecast demand for 2024/25 = 277,000,000` (quoted from source document notes for TFL-BUSINESS-PLAN-2019-12 in data/sources.yaml, not a loaded observation).

**Formula:**
```
drift_absolute = 652,000,000 - 1,037,000,000 = -385,000,000
drift_percent  = -385,000,000 / 1,037,000,000 × 100 = -37.1263%

Yield decomposition (notes only, not a separate drift row):
  demand_ratio   = 242,866,594 / 277,000,000 = 0.8768  (-12.32%)
  yield_forecast = 1,037m / 277m  = £3.744 per journey
  yield_actual   =   652m / 243m  = £2.685 per journey
  yield_ratio    = 2.685 / 3.744  = 0.7171  (-28.29%)
  combined: demand_ratio × yield_ratio = 0.6287 = 1 − 0.3713 (reconciles to revenue drift)
```

**Decisions made:**

- **Single row, direct comparison, no deflator.**
  - Alternatives considered: deflate both sides to a common price year (2019 forecast in 2019 prices; 2024/25 outturn in 2024/25 cash) for a real-terms restatement; insert the yield decomposition as two separate drift rows (demand-only and yield-only).
  - Decision: single row with direct comparison; yield decomposition captured in notes.
  - Reasoning: INVESTIGATION_BRIEF.md section 6.3 specifies direct comparison of forecast and actual in cash terms. A real-terms restatement is a Path B methodology refinement for a later unit. The yield decomposition is informative commentary rather than an independent drift finding; it shares the same comparison_date and same comparison_value (revenue outturn) as the headline drift, so separate rows would duplicate data.

- **Dual-baseline explanation captured in notes.**
  - Reasoning: assumption 2's drift row uses the 2011 Crossrail Business Case 200m demand "steady-state" forecast as the baseline; this revenue drift row uses the 2019 TfL Business Plan 277m forecast for 2024/25. Both are correct baselines for their respective assumptions. Without explicit explanation a reader could misread the +21% demand drift in assumption 2 and the -12% implied demand component in this row as contradictory. Notes capture the trajectory (2011 forecast → 2019 revised forecast → 2024/25 outturn) and instruct findings drafting to explain this rather than presenting only one number.

- **Definitional flag preserved from the observation's notes.**
  - Reasoning: the TfL QPR "Passenger income" line for the Elizabeth line is the value we compared against the 2019 plan's £1.037bn forecast. The definitional match between those two categories has not been independently verified. The drift row notes mark this as a methodology review question and state that the row is not suitable for use in a published finding until the match is verified.

- **Confidence: medium.**
  - Arithmetic is exact and reproducible. Headline drift is robust. Yield decomposition has a slight reproducibility discount because the 277m demand figure is from a source-document note rather than a loaded observation. Definitional flag is the main residual uncertainty.

**Caveats applied:**

- Caveat 2 (pandemic break in demand series): applies. The 2019 forecast was pre-pandemic; the outturn captures all pandemic and recovery effects on both yield and demand. A no-pandemic counterfactual for either component would require additional modelling not performed here.
- Definitional flag on "Passenger income" (QPR) vs 2019 Business Plan forecast category. Captured in notes; needs independent verification before a finding is drafted.
- Status: TfL QPR Q4 2024/25 is unaudited quarterly reporting. Subsequent audited figures from TfL's 2024/25 Annual Report could revise; revisions would load as new append-only rows with a later captured_at.
- No deflator applied. Different price bases are implicit between the 2019 forecast and the 2024/25 outturn. Not corrected at this framing level per brief section 6.3.

**Drift result:**

- Headline: drift_absolute -£385m; drift_percent -37.1263%.
- Yield decomposition: demand -12.32% vs 2019 plan forecast; yield per journey -28.29% vs 2019 plan implied yield; combined -37.13% (reconciles to the headline exactly).
- Direction: negative, robust under the method as specified.

**Confidence:** medium. Reasoning above.

**Notes for methodology.md:**

- methodology.md section 6.3 already specifies direct comparison of forecast and actual in cash terms; no rewrite needed.
- methodology.md should explicitly describe the yield decomposition as the supporting analysis that the revenue drift row carries in its notes, and state that the 277m demand figure for 2024/25 is drawn from a source-document note rather than a loaded observation.
- methodology.md should describe the dual-baseline issue (2011 Crossrail BC demand forecast vs 2019 TfL Business Plan demand forecast) and instruct that published findings reconcile the trajectory rather than presenting either number in isolation.
- methodology.md should preserve the definitional flag on "Passenger income" from QPR, with a direct reference to the TfL 2019 Business Plan for the category definition.

**What this tells us about drift patterns more generally:**

Revenue drift on fare-funded public services is a multiplicative composition of demand drift (journey volumes) and yield drift (average fare per journey). A finding that reports only the aggregate revenue drift without the decomposition is under-specified: the two components have different causal drivers (demand reflects economic conditions, travel patterns, and service quality; yield reflects fare policy, ticket mix, and concession structures) and different policy implications. For any service with fare-setting flexibility, the decomposition is the finding.

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

**Method applied:** Derive the restated VFM band from each of the three BCR scenarios in assumption 4 using the DfT VFM band mapping (band 1 poor BCR<1.5, band 2 medium 1.5-2.0, band 3 high 2.0-4.0, band 4 very high ≥4.0). One assumption-5 row per BCR scenario, preserving 1:1 parity with assumption 4's three rows.

**Observations used:**
- `crossrail_retrospective.assumptions.value = 2` (value_for_money_band, baseline band 2 medium) [baseline]
- Parent BCR values from assumption 4's three drift rows (database ids captured in per-row notes):
  - BCR 1.883250 (nominal cost ratio) → band 2
  - BCR 1.917550 (real no-correction) → band 2
  - BCR 2.061367 (real with 7.5% correction) → band 3

**Formula:**
```
band_code = discrete mapping from BCR value to {1, 2, 3, 4} per DfT TAG thresholds
drift_absolute = restated_band - baseline_band
drift_percent  = drift_absolute / baseline_band × 100  (ordinal-level, see caveat below)

Row 5a: BCR 1.883 → band 2; drift_abs 0; drift_pct 0.0000%
Row 5b: BCR 1.918 → band 2; drift_abs 0; drift_pct 0.0000%
Row 5c: BCR 2.061 → band 3; drift_abs +1; drift_pct 50.0000%
```

**Decisions made:**

- **Three rows, one per parent BCR scenario (Option 1).**
  - Alternatives considered: two rows aggregating by distinct band outcome; a single row encoding a range.
  - Decision: Option 1, three rows.
  - Reasoning: preserves 1:1 parity with assumption 4 so each band row traces to exactly one BCR scenario; keeps the outcome distribution explicit (two of three BCR scenarios produce no band change); supports clean extension if Scenario B is added later. The apparent duplication of headline outcome between rows 5a and 5b is honest rather than redundant.

- **Cross-reference parent BCR rows by id with query pattern in notes.**
  - Decision: each assumption 5 row carries the parent BCR drift_calculation id plus an inline SQL query pattern in its notes field.
  - Reasoning: makes the derivation chain self-traceable. A reader looking at any assumption 5 row can jump to the parent BCR row with one SQL query, without rebuilding the join from assumption 4.

- **Drift_percent is ordinal-level, not continuous-level. Disclosed on every row.**
  - Reasoning: drift_percent computed on band codes (integers 1-4) is mathematically well-defined (1/2 × 100 = 50% for row 5c) but conceptually misleading if read as a continuous drift metric. Every row's notes state: "drift_percent here is computed on band code (ordinal 1-4). Band-level drift = 0% does not imply zero underlying BCR drift; see parent assumption 4 drift_calculation row for continuous BCR drift." Row 5c's notes additionally emphasise that +50% band drift is a mechanical consequence of ordinal encoding, not a headline number.

- **Band change on row 5c is methodologically sensitive, not robust.**
  - Inherited from assumption 4's sensitivity disclosure. Row 5c's notes carry the full language: boundary at ~4.3% pre-2014 correction; 5-10% plausible range all yields band 3; 0% correction yields band 2. Findings must not read row 5c as a robust band change.

**Caveats applied:**

- All three rows inherit caveats from their parent BCR row in assumption 4.
- Row 5c specifically inherits the boundary-sensitivity language from assumption 4's real-with-correction row.
- Rows 5b and 5c both carry caveat 1 (ONS-OPI vs BCIS-TPI) via their parent BCR rows' real cost ratio. Row 5a does not (no deflator in parent).

**Drift result:**

- Three rows. Two at band 2 (drift 0); one at band 3 (drift +1).
- Direction: unchanged or upward. No downward band drift under any scenario.
- Robust finding: the restated BCR sits close to the medium/high boundary. Across all three scenarios, the restated band is either medium (2 of 3) or high (1 of 3); the boundary crossing is methodologically sensitive.
- Defensible one-line summary: "The restated BCR sits close to the medium/high band boundary; the band result is methodologically sensitive rather than robust, with two of three co-equal scenarios keeping the BCR in the medium band and one nudging into high."

**Confidence:** low on all three rows, inherited from parent BCR. Row 5c carries an additional boundary-sensitivity caveat.

**Notes for methodology.md:**

- Categorical findings derived from continuous metrics crossing externally imposed thresholds should always carry an explicit threshold-proximity disclosure.
- The DfT TAG bands are a published external reference frame; methodology.md should cite the TAG source and note that the band definitions themselves are subject to DfT revision over time. Current bands are from DFT-TAG-VFM per sources.yaml.
- The ordinal vs continuous drift_percent issue is generalisable. methodology.md should describe the distinction and state the investigation's convention: drift_percent is mechanically computed from baseline and comparison values regardless of unit type; readers must check the unit (count, gbp, ratio, band_code) to interpret drift_percent correctly.

**What this tells us about drift patterns more generally:**

Categorical findings have a different epistemic status than continuous findings. When a categorical finding depends on a continuous metric crossing an externally defined threshold, the strength of the categorical claim is bounded by the sensitivity of the continuous metric at the threshold. For Crossrail's BCR restatement, one of three co-equal scenarios crosses the 2.0 medium/high threshold, and it crosses by only 0.06 points; the other two scenarios fall below the threshold by 0.08-0.12 points. A reader treating "VFM band drifted medium to high" as a finding is overclaiming; the defensible finding is "the restated BCR sits close to the medium/high boundary with sensitivity-dependent band assignment." More generally: any drift analysis that maps a continuous metric through a discrete banding framework should report continuous drift as the primary finding, with the band change flagged as a secondary, sensitivity-dependent consequence rather than a headline.

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

---

## Session close

Session ended 2026-04-22 (originally opened 2026-04-21, closed across two calendar dates due to mid-session methodology correction).

### Rows inserted

| Assumption | Drift rows inserted | Status |
|---|---:|---|
| 1. construction_funding_envelope | 2 | computed |
| 2. passenger_journeys_full_opening | 1 | computed (decomposition deferred) |
| 3. revenue_2024_25 | 0 | deferred pending Ant's TfL data supply |
| 4. benefit_cost_ratio_dft | 3 | computed (Scenario B deferred) |
| 5. value_for_money_band | 3 | computed |
| **Total** | **9** | |

### One-line findings summary per assumption

Framed honestly, with sensitivity flags where applicable. **Not headline findings; raw drift results.** Findings drafting is a separate unit.

1. **construction_funding_envelope:** real-terms overspend of approximately £2.5-3.7bn (+15% to +25%) against the 2010-11 baseline, depending on whether a 7.5% pre-2014 construction-inflation correction is applied to the baseline. Materially smaller than the +28% nominal cash overrun headline cited in PAC-CROSSRAIL-2021. Direction robust under the corrected deflation method; magnitude sensitive to index choice (caveat 1) and pre-2014 correction magnitude.

2. **passenger_journeys_full_opening:** headline drift of +21.43% (242.9m outturn vs 200m forecast). Likely UNDERSTATES the eventual steady-state drift because 2024/25 is year three of operation and the ramp-up has not completed. Caveat 2 (pandemic break) decomposition deferred; headline conflates pre-pandemic trend drift and post-pandemic recovery dynamics. Direction robust; magnitude a lower bound.

3. **revenue_2024_25:** deferred this session. TfL primary-source values not loaded. London Assembly cross-reference (£606m 2023/24) suggests substantial negative drift vs the £884m 2023/24 forecast point; 2024/25 full-year is expected to be similarly below the £1.037bn forecast, but precise figures must come from TfL primary sources. Follow-up: separate small session on supply of three TfL Annual Report values with primary citations.

4. **benefit_cost_ratio_dft (three co-equal scenarios, Scenario A only):**
   - Nominal cost ratio: restated BCR 1.88 (drift -4.40%).
   - Real cost ratio, no pre-2014 correction: restated BCR 1.92 (drift -2.66%).
   - Real cost ratio, 7.5% pre-2014 correction: restated BCR 2.06 (drift +4.64%).
   - Direction mixed across the three co-equal scenarios; restated BCR in the range 1.88-2.06. Scenario B deferred. Not a full NPV reconstruction.

5. **value_for_money_band:** two of three scenarios keep the BCR in band 2 (medium, 1.5-2.0, no band change); one scenario nudges the BCR just above 2.0 into band 3 (high). Band-change finding is methodologically sensitive rather than robust; boundary at approximately 4.3% pre-2014 correction. Honest summary: "restated BCR sits close to the medium/high band boundary with sensitivity-dependent band assignment."

### Open methodological questions surfaced during the session

All recorded under "Open questions" above. Summary:

- **Caveat 2 decomposition for assumption 2.** Requires a London rail proxy series (ORR TfL Underground, or similar TOC journeys series) covering 2011-2019 to estimate the no-pandemic counterfactual. Not loaded in this session. Follow-up unit of work.
- **Scenario B for assumption 4.** The "plausible long-run demand trajectory consistent with the first three years of operation" is a judgement call requiring separate framing (linear extrapolation, exponential decay to peak, match to comparable line openings, etc.). Methodology question rather than computation.
- **Headline strength threshold for categorical findings.** When does a categorical finding (e.g. band change) sitting near a threshold boundary become a defensible headline? Sits as a candidate input for methodology-shared.md in the umbrella repo.

### Cross-cutting decisions recorded

- **Corrected deflation method for assumption 1.** INVESTIGATION_BRIEF.md section 6.1 specified a one-sided reprice (baseline to current prices, outturn in cash) that produces direction-sensitive results. Corrected method puts both sides in 2010-11 prices (proxied by Jan 2014 prices in practice) using ONS-OPI-INFRA-NEW as the deflator. INVESTIGATION_BRIEF.md will need updating in a separate commit once the corrected method is finalised.

### Recommended next steps

**For the methodology.md writing session (next unit):**

- methodology.md must describe the corrected deflation method for assumption 1, replacing the flawed one-sided reprice in the current brief.
- methodology.md must describe the ordinal vs continuous drift_percent distinction and the band-at-boundary sensitivity framing.
- methodology.md must cite this decisions log as the source record for methodological choices made during drift computation.
- methodology.md must list the deferred computations (assumption 3; caveat 2 decomposition for assumption 2; Scenario B for assumption 4) with their unblocking requirements.
- methodology.md section numbering per INVESTIGATION_BRIEF.md was 6.1-6.5; the corrected method keeps the same outline but fixes the computational step specified in 6.1.

**For the TFL-EL-REVENUE follow-up:**

- Required input: three TfL Annual Report values for Elizabeth Line annual passenger income for fiscal years 2022/23, 2023/24, and 2024/25, each with primary TfL citation (document title, section or page, and date). Source URLs already captured in data/external_series.yaml for TFL-EL-REVENUE.
- Required action: load into pda_shared.external_observations under TFL-EL-REVENUE using the same ingest pattern (YAML provenance file + per-row SQL, committed together).
- Expected output: one drift row for assumption 3 (direct comparison of £1.037bn December 2019 forecast against 2024/25 outturn), similar shape to assumption 2.

**For the Scenario B follow-up (assumption 4):**

- Required input: an explicit methodology statement for "plausible long-run demand trajectory". Candidates include (i) linear extrapolation of observed 2022/23-2024/25 growth rate; (ii) logistic curve fitting to a specified peak; (iii) matching to comparable line openings (e.g. Jubilee Line extension, London Overground). Choice is a judgement call rather than a computation.
- Required action: document the chosen trajectory and apply it as an alternative demand ratio in a new assumption-4 row (with corresponding assumption-5 row).
- Expected output: one additional assumption-4 row and one additional assumption-5 row, bringing totals to 4 + 4 = 8 across those two assumptions.

**For the caveat 2 decomposition (assumption 2):**

- Required input: a loaded London rail proxy series covering 2011-2019. Most defensible candidates are ORR-published TfL Underground annual journeys (via the same Table 1223 file's predecessor sub-tables or a separate TfL publication) or a GB-wide passenger journeys trend that could be scaled to London.
- Required action: load the proxy series using the existing ingest pattern; compute the 2011-2019 trend; project it to 2024/25 without a pandemic; compare against actual 242.9m to decompose total drift into trend and recovery components.
- Expected output: two additional assumption-2 rows (trend drift; recovery drift).

**For INVESTIGATION_BRIEF.md update:**

- Section 6.1 needs revision to reflect the corrected deflation method. This is a cross-cutting decision already recorded above. The update should be a small separate commit on its own branch once the corrected method is finalised.

### End of session.

---

## Independent review

The methodology and the drift calculations produced from it were reviewed on 2026-04-22 by an independent domain expert in public-sector programme assurance, consistent with the reviewer profile set out in `methodology.md` §6.1 and `INVESTIGATION_BRIEF.md`'s review-and-attribution section.

**Review date (verbal approval):** 2026-04-22.

**Review outcome:** clean approval, no material changes requested.

**Formal write-up:** pending. The reviewer indicated at the time of verbal approval that a formal write-up will follow. When received, it will be recorded in `pda_shared.reviews`. Reviewer metadata sits in `pda_shared.reviewers` (service-role only, `consent_to_name = false`).

**Publication gate:** remains closed until the formal write-up is recorded in `pda_shared.reviews`. Findings drafted in the subsequent findings session are inserted into `crossrail_retrospective.findings` with `published = false`. They become publishable when the formal review row lands.

---

## Findings drafting

### Finding 1: cost_real_terms_residual

**Drafted:** 2026-04-22.
**Finding id in Supabase:** `28fe3fe9-f5e5-4f6d-b8ec-5553fc1bac4c`.
**Published:** false (publication gated on formal review write-up).
**Title:** *Crossrail's real-terms cost overrun is approximately £2.5-3.7bn, smaller than the 28% cash headline*.
**Supporting drift rows:** `87ef17ea-3163-4998-aa06-5fbb74d29461` (assumption 1 Row A, unadjusted, +24.75%) and `eca92970-94a6-470c-a4e5-f29ed1f3807b` (assumption 1 Row B, 7.5% pre-2014 correction, +16.05%).
**Confidence:** medium. Direction robust; magnitude bounded by the pre-2014 correction range (not by the ONS vs BCIS index choice, which is flagged as a separate constraint in the caveats).

**Drafting decisions:**

- **Title choice.** Three candidates considered; Option A ("Crossrail's real-terms cost overrun is approximately £2.5-3.7bn, smaller than the 28% cash headline") selected because it quantifies the real-terms residual and contrasts directly against the PAC 2021 cash-overrun figure in the public record. Option B emphasised the inflation fraction; Option C was a shorthand without the cash-overrun contrast.
- **Arithmetic correction caught during drafting.** The original Step 3 proposal framed the headline as "approximately three-quarters explained by construction inflation". That was arithmetically backwards: the inflation component is 10-40% of the cash overrun, not three-quarters, and the real-terms component is 60-90%. The error was caught and the title reframed before any draft landed in the database. Recorded here as a discipline reminder: framing direction must be verified against the arithmetic before any headline is proposed. The check applies to every subsequent finding.
- **Opening paragraph reordering.** First draft led with the PAC cash overrun figure as the opening sentence. Revised at Ant's direction to lead with the finding (the real-terms residual range) and use the cash figure as context. Rationale: a journalist quoting the finding should quote the investigation's conclusion, not the public-record figure the investigation is qualifying.
- **Magnitude field scope.** Short form ("residual of £2.5bn to £3.7bn (+15% to +25%) in real terms against the 2010-11 baseline") stored in the structured field. The cash-overrun contextualisation lives in the narrative, not in the structured field.

**Arithmetic checks performed before insertion:**

- Real / cash overrun ratio: Row A 24.75/28 = 88.4%; Row B 16.05/28 = 57.3%. Range "60-90% real, 10-40% inflation" used in the narrative rounds from the computed 57-88%.
- Drift row reconciliation: Row A residual £3,663,709,875.03 and Row B residual £2,553,709,875.03 reconcile to the reported "£2.5bn to £3.7bn" range.
- Outturn figure £18.8bn matches the NAO-CROSSRAIL-2021 citation in both drift rows' notes.

**Notes for article drafting and for the reviewer:**

- Candidate article opener. The contrast with PAC 2021 framing is the narrative hook.
- The ONS-OPI vs BCIS-TPI caveat is the one most likely to be pressed by a programme-assurance reviewer. The caveats field carries the full position.
- The range (£2.5bn to £3.7bn) is a real analytical range, not a rhetorical hedge; both rows are co-equal drift calculations with different pre-2014 treatments, not a best-estimate plus sensitivity.

### Finding 2: revenue_shortfall_decomposition

**Drafted:** 2026-04-22.
**Finding id in Supabase:** `aa83b45e-8945-40b3-b50f-0870e8012045`.
**Published:** false.
**Title:** *Revenue shortfall decomposes: demand down 12%, yield down 28%*.
**Supporting drift rows:** `cf423e0d-cd41-4625-b297-99679e447c7d` (assumption 3 single row, −37.13% revenue drift vs the 2019 TfL Business Plan forecast for 2024/25).
**Confidence:** medium. Arithmetic exact; direction robust; residual uncertainty in the two caveats (definitional match, pandemic-era components).

**Drafting decisions:**

- **Title kept from Step 3 proposal.** "Revenue shortfall decomposes: demand down 12%, yield down 28%" is specific and directly replicable; the two numbers in the title let a reader match against the finding body without re-computing. No revision flagged.
- **Multiplicative framing with additive sanity.** The decomposition is stated multiplicatively (demand ratio × yield ratio = revenue ratio) in both the narrative and the magnitude field. An additive cross-check ran before drafting: demand-only effect −£128m, yield-only effect −£293m, interaction +£36m, summing to −£385m. Yield dominance holds on both the ratio comparison (|−28.3%| > |−12.3%|) and the additive share (£293m ≈ 76% of the gap vs £128m ≈ 33%; interaction accounts for the balancing fraction). This cross-check is not in the narrative (multiplicative framing is cleaner for a reader) but is recorded here as part of the arithmetic discipline.
- **Softened the pandemic causal claim.** First draft asserted that yield per journey was reduced by the pandemic-era shift toward off-peak and leisure travel. Revised at Ant's direction to hedge the claim ("may reflect ... including possible shifts toward off-peak and leisure travel") because the investigation does not directly substantiate the causal mechanism. The revision aligns with the explicit non-assertion of the fare-policy hypothesis elsewhere in the caveats paragraph.
- **Removed "materially" from paragraph 1.** "Each journey generates materially less revenue" became "each journey generates less revenue". The numbers (£2.68 vs £3.74) carry the claim; the adjective was redundant.
- **Causal hypothesis disclosed but not asserted.** The yield-dominant split points toward a fare-policy question (Mayoral fare freeze, Elizabeth Line fare structure relative to the Underground). The finding names this as a hypothesis that the investigation does not substantiate and flags it for Laura's review rather than asserting it.

**Arithmetic checks performed before insertion:**

- Multiplicative reconciliation at 10-decimal precision: 0.876775 × 0.717102 = 0.628746, matching 652/1037 = 0.628737 with a residual of 0.0000088 attributable to rounding in the two-decimal-place unit yield values used in the narrative. At the drift row's 6-decimal storage precision, reconciliation is exact.
- Additive decomposition (sanity): demand-only −£127.8m, yield-only −£293.3m, interaction +£36.1m, sum −£385.0m, matches drift_absolute.
- Yield dominance on both views: 28.3% > 12.3% in magnitude; 76% > 33% in additive share.

**Notes for article drafting and for the reviewer:**

- Likely second finding in the article, following finding 1 (the cost real-terms residual).
- The definitional flag on "Passenger income" is the main thing Laura's formal review should verify.
- The 277m demand figure used in the decomposition is from a source document note, not a loaded observation. A reader reproducing the decomposition from observations alone cannot reconstruct the split without loading TFL-BUSINESS-PLAN-2019-12's demand forecast as an observation (which would require separate extraction from the plan document). This is a known limitation of the current reproducibility path.

### Finding 3: bcr_near_offset

**Drafted:** 2026-04-22.
**Finding id in Supabase:** `ded28030-def9-4244-a8ef-a67d1263dd59`.
**Published:** false.
**Title:** *Cost overrun and demand over-performance near-offset on value for money*.
**Supporting drift rows:** six rows. Three BCR rows (`dbdb2a55-0b21-458a-8115-c1bb2f36d45e` nominal 1.883, `5a263b34-1b89-4727-b05e-87092168a30f` real no-correction 1.918, `3d89f5f1-e741-4cce-875d-0cc7b99d49cd` real 7.5% correction 2.061) and three band rows (`8897fe80-1018-4f11-88dd-d99555113ed8` band 2 from BCR 1.883, `3af9a0bb-90bf-434a-ac3d-dca697341df9` band 2 from BCR 1.918, `916d11c9-1bfa-4b3a-b519-9e07188f9104` band 3 from BCR 2.061).
**Confidence:** low. Reflects the combined weight of the sensitivity-only framing, the benefits-linear-in-demand simplification, the inherited caveats 1 and 2, and the deferred Scenario B and caveat 2 decomposition. The low confidence is a methodological-level statement, not an arithmetic-uncertainty statement; the arithmetic is exact and the direction within the corrected method is robust.

**Drafting decisions:**

- **Title kept from Step 3.** "Cost overrun and demand over-performance near-offset on value for money". Specific and directional without overclaiming.
- **Long-form length.** ~960 words, within the 800-1,200 target. Justified by the synthesis nature of the finding, the need to reconcile with finding 1 (the "tension"), the three co-equal scenarios each needing brief explanation, and the band-boundary sensitivity warranting prominent disclosure.
- **Quantified band-boundary threshold.** Algebra worked out before drafting: the restated BCR crosses 2.0 at a pre-2014 correction of approximately 4.303%. The narrative rounds to "approximately 4.3%". The plausible 5-10% range all sits above this threshold; the critical observation is that the band outcome flips between nominal/no-correction (band 2) and any real-corrected variant within the plausible range (band 3).
- **Tension with finding 1 framed as consistency, not contradiction.** First draft used "in tension in a useful way" which was informal. Revised at Ant's direction to "address different questions and are consistent with each other" which precisely names the relationship (cost-overrun finding and BCR-near-offset finding measure different things; both are true).
- **Weak vs strong reading of the finding surfaced explicitly in the final paragraph.** The strong reading ("value-for-money categorisation has not clearly changed") is the investigation's finding. The weak reading ("remained on budget for value for money") is disclaimed with scare quotes; kept in because it is the kind of formulation that could appear in coverage if the finding were over-interpreted.
- **supporting_drift_ids scope confirmed at six rows.** Per Step 3 approval: the three BCR rows and three band rows are the direct support. Upstream assumption 1 A/B rows and the assumption 2 row are referenced by ID inside the narrative and via the BCR rows' parent-row notes; they are not duplicated as direct supporting rows.
- **Caveats field uses lettered enumeration (a-d).** Four caveats each carry weight; enumeration helps a reader check each one. Lettering mirrors the style used in finding 2's caveats field.

**Arithmetic checks performed before insertion:**

- Three BCR values reconcile to the formula `restated_BCR = 1.97 × 1.21433 / cost_ratio` using the three cost ratios from the Step 3 schema.
- Midpoint of [1.883, 2.061] is 1.972; 1.97 is 0.002 off the exact arithmetic midpoint. Narrative says "almost exactly in the middle" — justified.
- Band-crossing threshold: solving `2.0 = 1.97 × 1.21433 / cost_ratio` yields `cost_ratio = 1.19612`, which corresponds to `adjusted_baseline = £15.437bn`, which is `£14.8bn × 1.04303`. Pre-2014 correction of 4.303% is the boundary. Rounded to 4.3% in the narrative.
- Directional sanity: each scenario's BCR drift direction matches the sign of (demand_ratio - cost_ratio). Nominal (cost 1.270 > demand 1.214): BCR down (-4.4%). Real no-correction (cost 1.248 > demand 1.214): BCR down (-2.7%). Real 7.5% (cost 1.161 < demand 1.214): BCR up (+4.6%). All three align with the stored drift rows' signs.
- Tension with finding 1 sanity: the real-terms cost overrun (+15-25%) and the BCR near-offset (restated 1.88-2.06) are compatible because demand also moved +21% in the same direction. No contradiction.

**Notes for article drafting and for the reviewer:**

- Likely article conclusion. The synthesis with finding 1 is the investigation's richest insight.
- The band-boundary sensitivity is the specific thing that needs careful framing in any published version: stating "Crossrail moved into the high VFM band" would be overclaiming, because only one of three co-equal scenarios shows the band change, and the change depends on the pre-2014 correction magnitude.
- Laura's formal review should particularly scrutinise the benefits-linear-in-demand simplification. This is the single largest methodological approximation in the finding. If her judgement is that the simplification is acceptable for a sensitivity-only framing, the finding stands as drafted. If she flags it as too strong an approximation, the finding narrative would need to add language around that specifically.
- The low-confidence rating is methodological and reflects the sensitivity-only framing; it is the correct rating for the genre of calculation. Not a hedge.

---

## Session close: findings drafting

**Session date:** 2026-04-22.

**Findings inserted:** three, all with `published = false`.

| Finding key | Title | Confidence | Supporting drift rows |
|---|---|---|---|
| `cost_real_terms_residual` | Crossrail's real-terms cost overrun is approximately £2.5-3.7bn, smaller than the 28% cash headline | medium | 2 |
| `revenue_shortfall_decomposition` | Revenue shortfall decomposes: demand down 12%, yield down 28% | medium | 1 |
| `bcr_near_offset` | Cost overrun and demand over-performance near-offset on value for money | low | 6 |

Supabase `crossrail_retrospective.findings` row count: 3. All three rows carry `published = false`. Publication gate remains closed until the formal reviewer write-up is recorded in `pda_shared.reviews`.

**Drafting discipline observations:**

- Arithmetic discipline caught a framing error on finding 1 before insertion (the "three-quarters explained by construction inflation" formulation was backwards; corrected to "60-90% real, 10-40% inflation"). Recorded as a discipline reminder in the finding 1 entry above and applied to findings 2 and 3. For future findings drafting sessions in any PDA Investigations case, the discipline is: verify the direction of framing against the arithmetic before proposing a headline, not after.
- Causal-mechanism claims softened on finding 2 ("may reflect pandemic impact ... including possible shifts toward off-peak and leisure travel" rather than asserting the shift). Consistent with the explicit non-assertion of the fare-policy hypothesis in the same paragraph.
- Tension between findings 1 and 3 framed as consistency-with-different-questions rather than contradiction, following a refinement request by Ant. The two findings measure different things and both are true.
- Each finding's long-form narrative carries the drift-row IDs by UUID. A reader who wants to reproduce the arithmetic has a direct path from the narrative to the underlying rows in `crossrail_retrospective.drift_calculations`.
- Word counts: finding 1 ~370 (medium), finding 2 ~378 (medium), finding 3 ~960 (long). All within the Step 3 targets.

**Publication gate status at session close:**

Closed. Three findings sit in `crossrail_retrospective.findings` with `published = false`. Laura's formal methodology write-up is the unblocker; on receipt, a separate (small) unit of work will insert a reviewer row into `pda_shared.reviewers`, a review row into `pda_shared.reviews`, and flip the three findings' `published` flag to true (subject to Laura's review outcome per-finding, since a review that flags any particular finding for revision would pause that finding's publication specifically).

**Session end.**
