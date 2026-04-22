# Methodology

This document is the operational methodology for the Crossrail retrospective drift analysis. It specifies how each of the five assumptions in `data/assumptions.yaml` is scored against public external data, and what the resulting rows in `crossrail_retrospective.drift_calculations` represent.

The document sits alongside `INVESTIGATION_BRIEF.md` (which sets out the investigation's question, anchor, and caveats) and `analysis/drift-decisions-log.md` (which records methodological decisions in the order they were made during the drift calculations session). Programme-level standards, including reproducibility, append-only data, independent review, licensing, and tooling, are covered in the umbrella `../pda-investigations/methodology-shared.md` and apply here without restatement.

## 1. Purpose and scope

This methodology covers how five published assumptions from the 2011 Crossrail Business Case (and one forecast from the 2019 TfL Business Plan) are compared against current public data to quantify drift. The comparisons produce ten drift calculation rows distributed across the five assumptions.

The methodology does not cover:

- A full NPV reconstruction of the Crossrail benefit-cost ratio. That is explicitly out of scope, requires TfL's internal appraisal model, and is not available from public data. The BCR restatement in this investigation is a sensitivity-only calculation.
- A restatement of the 2011 business case in its entirety. Only the five numerical assumptions listed in the brief are scored.
- Drift analysis for Crossrail 2, HS2, or any other programme. The scope is strictly the completed Crossrail programme as delivered in the Elizabeth Line.
- Policy recommendations about future major rail programmes.

The methodology is written for three audiences simultaneously: the independent methodology reviewer (who will check whether the choices are defensible), a journalist or researcher citing any finding (who needs enough detail to verify the claim), and a future PDA Investigations reader applying similar methods (who needs operational guidance transferable to other cases).

## 2. Conventions and data model

Drift calculations are stored in `crossrail_retrospective.drift_calculations`, one row per scoring. The table is append-only. If a calculation is ever re-run with different inputs, a new row is inserted with a later `captured_at`; the previous row is preserved.

Each row carries:

- `assumption_id` and, where applicable, `series_id` (nullable for compound calculations such as the BCR and band rows that combine multiple series)
- `baseline_value` and `baseline_date`: the assumption's value as published, in the price base applicable to the calculation
- `comparison_value` and `comparison_date`: the external observation or derived value being compared against the baseline, in the same price base
- `drift_absolute` and `drift_percent`: the numeric drift
- `methodology_notes`: a compact statement of the method applied
- `confidence`: high, medium, or low, with reasoning captured in notes
- `notes`: the full provenance, caveats, cross-references, and interpretation context

A note on `drift_percent`. The `drift_calculations` table stores drift_percent as a single numeric column regardless of the unit of the underlying values. For continuous metrics (count, gbp, ratio) drift_percent is the conventional relative change and is interpretable as such. For ordinal metrics (specifically `band_code` in assumption 5, an integer 1-4 mapping to DfT value-for-money bands) drift_percent is mechanically computed but not continuous: a row showing 50% band drift indicates one band-position movement on a four-band scale, not a 50% continuous change in value for money. Each band-drift row in assumption 5 carries this clarification in its notes field. A reader interpreting drift_percent must check the unit of the assumption being scored.

Baseline and comparison dates follow conventions that depend on whether a price-base adjustment is applied:

- Where no price-base adjustment is applied (assumptions 2, 3), dates on the row are the original dates: the baseline date from `assumptions.baseline_date`, the comparison date from the observation.
- Where a price-base adjustment is applied (assumption 1, and by inheritance in assumption 4's real-cost scenarios), the stored dates reflect the price base of the stored values. Original dates are captured in the notes field.

Source citations appear in two places. Each observation in `pda_shared.external_observations` carries its source in its own notes field and in `data/observations/<series>.yaml`. Each drift row references the observations it uses by series code and observation date, and names the primary source document (for example NAO-CROSSRAIL-2021) inline where a comparison value is a published figure rather than a loaded observation.

## 3. Method by assumption

### 3.1 Construction cost, real-terms comparison (primary)

**What is being scored.** The £14.8bn funding envelope committed in the July 2011 Crossrail Business Case Update Summary Report, against the approximately £18.8bn cash outturn reported by the National Audit Office in July 2021 (NAO 2021, "Crossrail: a progress update", HC 10 Session 2021-22). The question being asked is: of the approximately £4bn gap between baseline and outturn, how much is explained by construction-sector inflation over the programme's life, and how much is a real-terms residual?

**Baseline.** £14,800,000,000 in 2010-11 prices, baseline date 2011-07-01, from `crossrail_retrospective.assumptions` (`assumption_key = construction_funding_envelope`).

**Comparison.** £18,800,000,000 cash, settled December 2020 per NAO 2021. This figure is not a loaded observation but a published settled outturn; it is cited in the drift rows' notes fields with the NAO source reference.

**Deflator.** ONS Construction Output Price Index for Infrastructure (new work, 2015=100), series code `ONS-OPI-INFRA-NEW` in `pda_shared.external_series`. The series begins in January 2014. The pre-2014 period is covered by the superseded BIS Construction Output Price Index, which ONS publishes linking factors for but which is not loaded as a separate series in this investigation.

**Method.**

Both sides of the comparison are expressed in January 2014 prices. The cash outturn is deflated back from its spend-weighted midpoint using a single-proxy-year approach. The proxy year is calendar 2017, chosen as an approximate midpoint of the 2014-2019 bulk of programme spend (Crossrail's construction peak was 2014-2018, with subsequent completion works 2018-2022). The deflator is the ratio of the January 2014 index value to the mean of the twelve calendar-2017 monthly index values.

Formally:

```
deflator         = ONS-OPI-INFRA-NEW[2014-01-31] / mean(ONS-OPI-INFRA-NEW, 2017)
                 = 100.2 / 102.025
                 = 0.982112
deflated_outturn = 18,800,000,000 × 0.982112
                 = 18,463,709,875.03   (£, Jan 2014 prices)
```

The baseline is in 2010-11 prices. The ONS series does not reach back to 2011-07 (its current publication begins 2014-01), so a direct deflation of the baseline to the same price base is not possible without loading a separate series. The methodology resolves this with two co-equal rows that represent the ends of a plausible range:

- **Row A (pre-2014 gap unadjusted).** The baseline £14.8bn is compared in Jan 2014 prices without adjustment. January 2014 is used as a proxy for 2010-11 prices. This understates the true Jan-2014 price of the baseline by approximately 5 to 10 percentage points, since construction inflation between 2011-07 and 2014-01 is not applied.

- **Row B (pre-2014 correction, 7.5%).** The baseline £14.8bn is rolled forward by 7.5% cumulative to approximate its value in Jan 2014 prices: 14,800,000,000 × 1.075 = 15,910,000,000. The 7.5% figure is the midpoint of a 5 to 10% range (approximately 2.9% annual compound inflation over 2.5 years, consistent with the publicly documented BIS Construction OPI Infrastructure trajectory for 2011-2014).

For each row, the residual is the deflated outturn minus the baseline (adjusted or not), in the common January 2014 price base:

```
Row A:  residual = 18,463,709,875.03 − 14,800,000,000     = +£3,663,709,875.03  (+24.75%)
Row B:  residual = 18,463,709,875.03 − 15,910,000,000     = +£2,553,709,875.03  (+16.05%)
```

**Decisions and alternatives considered.**

*Why deflate the outturn rather than reprice the baseline.* An earlier specification in `INVESTIGATION_BRIEF.md` section 6.1 required repricing the baseline to current prices while leaving the outturn in cash. Implementing this produced a result whose direction depended on the reprice target date (negative at 2025, positive at 2017, positive at 2020), rather than on any underlying fiscal fact. Both sides must be in the same price base for the residual to be a fact about the programme rather than an artefact of the choice. The corrected method expresses both sides in January 2014 prices by deflating the outturn. The cross-cutting decision is recorded in `analysis/drift-decisions-log.md`.

*Why a single proxy year rather than year-by-year deflation.* A year-by-year deflation would require an annual spend profile for the £18.8bn outturn, which is not cleanly available from public NAO or IPA reports (those reports describe cumulative spend and headline overruns rather than year-by-year attribution). The precision gained from year-by-year deflation is likely within the other uncertainty bounds in this calculation (the pre-2014 gap, the index choice per caveat 1). The single-proxy-year approach is simpler, fully reproducible from loaded ONS data, and consistent with the investigation's order-of-magnitude framing.

*Why calendar 2017 as the proxy year.* Crossrail's construction peak was 2014-2018, with significant completion-phase spend through 2019-2022 and some residual works after. The spend-weighted midpoint of the full programme life sits at approximately 2016-2017. The ONS-OPI-INFRA-NEW index is close to its 2014-2018 rolling mean at the calendar 2017 mean (102.025 vs a rolling mean of 102.85), so the choice is robust to small year shifts. A twelve-month mean is used rather than a single 2017 month to reduce sensitivity to the particular month chosen.

*Why 7.5% for the pre-2014 correction rather than a loaded BIS series.* The BIS Construction OPI predecessor series is available via ONS-published linking factors but is not loaded in this investigation. 7.5% cumulative corresponds to approximately 2.9% annual compound inflation over 2.5 years, which is consistent with the publicly documented BIS Construction OPI Infrastructure trajectory for that period. Loading the BIS series would permit a more precise figure; the 7.5% estimate is sufficient for the order-of-magnitude residual range this investigation reports, and is flagged as a refinement candidate for future iterations.

*Why two rows rather than one or three.* Reporting a single row with either the unadjusted or the corrected baseline would privilege one defensible choice over another. Reporting three rows (unadjusted, 5% correction, 10% correction) would spuriously imply greater precision than the method supports. Two rows at the ends of the stated plausible range are the cleanest expression of the real uncertainty.

**Output.**

Two rows in `crossrail_retrospective.drift_calculations`, linked to `assumption_key = construction_funding_envelope`. Row A stores the unadjusted result (baseline £14.8bn, residual +£3.66bn). Row B stores the 7.5%-corrected result (baseline £15.91bn, residual +£2.55bn). Both rows carry `baseline_date = 2014-01-31` and `comparison_date = 2014-01-31` to reflect the price base of the stored values; the original dates (2011-07-01 for baseline, 2020-12-31 for outturn settlement) are captured in the notes field.

The reporting range is a residual of approximately £2.5 to £3.7bn in real terms, corresponding to approximately 15% to 25% overspend against the 2010-11 baseline.

**Confidence.** Medium. The arithmetic is exact and reproducible from loaded ONS data. The direction (positive residual, real-terms overspend) is robust across the range of defensible methodological choices within the corrected method. The magnitude depends on three sources of uncertainty: the proxy-year choice for the deflator (bounded), the pre-2014 gap treatment (captured by the two-row structure), and the index choice between ONS-OPI-INFRA-NEW and BCIS-TPI (caveat 1, not captured in the reporting range because BCIS is subscription-restricted).

### 3.2 Passenger demand at full opening

**What is being scored.** The 2011 Crossrail Business Case forecast of approximately 200 million annual passenger journeys on the completed Elizabeth Line at steady state, against the ORR-reported outturn for fiscal year 2024/25 (242.9 million journeys).

**Baseline.** 200,000,000 annual journeys, baseline date 2011-07-01, from `crossrail_retrospective.assumptions` (`assumption_key = passenger_journeys_full_opening`). The figure is a rounded steady-state forecast derived from the detailed demand modelling underpinning the business case, confirmed in the NAO 2014 Crossrail report (HC 965).

**Comparison.** ORR-EL-JOURNEYS observation at 2025-03-31 = 242.866594 million journeys, representing fiscal year April 2024 to March 2025, provisional per ORR. Loaded from ORR Table 1223a (passenger journeys by operator, annual) as published in the March 2026 release.

**Method.**

Direct count comparison. No deflator, no price base, no transformation:

```
drift_absolute = 242,866,594 − 200,000,000 = +42,866,594
drift_percent  = 42,866,594 / 200,000,000 × 100 = +21.4333%
```

The comparison is stored in the assumption's unit (absolute count), converted from the ORR series unit (count_millions) at the point of drift calculation: 242.866594 × 1,000,000 = 242,866,594 exactly, preserving precision.

**Decisions and alternatives considered.**

*Why a single headline row rather than a decomposed calculation.* The 2011 forecast predates the pandemic. The observed outturn reflects both pre-pandemic trend drift (what demand might have been at 2024/25 if the programme had delivered on its 2011 timetable and no pandemic had occurred) and post-pandemic recovery dynamics. A proper attribution between the two components requires a London rail proxy series covering 2011-2019 to estimate the no-pandemic counterfactual trajectory. No such proxy is loaded in `pda_shared.external_observations`. An ad hoc decomposition against a GB-total rail journeys series would be defensible-looking but methodologically weak, because GB total includes long-distance intercity travel with quite different demand drivers. The methodology therefore reports the headline drift with the decomposition deferred and its dependency stated. This is documented as an open question in `analysis/drift-decisions-log.md` and in section 5.1 of this document.

*Why compare 2024/25 rather than a later year.* 2024/25 is the latest full fiscal year for which ORR has published outturn data at the time of this investigation. It is also the year anchoring the 2019 TfL Business Plan revenue forecast used in assumption 3, so using the same year for both keeps the investigation internally consistent across assumptions.

**Output.**

One row in `crossrail_retrospective.drift_calculations`, linked to `assumption_key = passenger_journeys_full_opening`. `baseline_date = 2011-07-01` and `comparison_date = 2025-03-31`. No price-base adjustment applies, so the row uses the original dates.

**Confidence.** Medium. The arithmetic is exact and reproducible from the loaded ORR observation. The direction (positive drift, outturn exceeding forecast) is robust. The magnitude of +21.4% is a lower bound on the true drift between the 2011 forecast and eventual realised steady-state demand for two reasons.

First, the 2011 forecast is specified at "full opening, steady state". The Elizabeth Line opened to passengers in May 2022. Fiscal year 2024/25 is year three of operation, with demand still growing year-on-year per the latest ORR data (quarterly journeys have continued to rise through 2025/26). The eventual steady-state figure, whenever it is reached, is likely higher than 242.9 million, which would make the drift larger than +21.4%.

Second, the caveat 2 decomposition is deferred. If a no-pandemic counterfactual trajectory for 2011-2024 were constructed, it would very likely sit above a simple linear extension of pre-2019 London rail demand (which itself was growing), and the implied "pre-pandemic drift" of the 2011 forecast against that counterfactual could be materially larger than +21.4% on its own.

Both directions of uncertainty point the same way: the real drift is likely larger than the headline +21.4%. The headline is therefore a defensible lower bound, not a best estimate.

**What this tells us.** Demand forecasts stated "at steady state" can be over-performed in the headline comparison yet still understate the real drift if the outturn is measured during ongoing ramp-up. For programmes with long ramp-up phases (rail, large-footprint retail, power), a drift analysis that compares a steady-state forecast against a non-steady-state outturn systematically understates positive drift. This is a distinct axis of methodological risk from the nominal-vs-real framing that appears in cost drift analysis. Both need explicit disclosure.

### 3.3 Annual passenger revenue, 2024/25

**What is being scored.** The 2019 TfL Business Plan forecast of £1.037bn in Elizabeth Line passenger income for fiscal year 2024/25, against the 2024/25 outturn of £652m reported in the TfL Quarterly Performance Report Q4 2024/25 (PUB25_029, published May 2025).

**Baseline.** £1,037,000,000 in 2019 prices, baseline date 2019-12-17, from `crossrail_retrospective.assumptions` (`assumption_key = revenue_2024_25`). This is the last comprehensive pre-pandemic published revenue forecast for the Elizabeth Line. The underlying ramp was £173m (2020/21), £240m (2021/22), £489m (2022/23), £884m (2023/24), £1.037bn (2024/25). A later post-pandemic restated forecast exists but was significantly lower; the 2019 forecast is used because it represents the clearest published "what did we think this would look like before a pandemic" reference point.

**Comparison.** TFL-EL-REVENUE observation at 2025-03-31 = 652 (in `gbp_millions`), converted to 652,000,000 in `gbp` at the point of drift calculation to match the assumption's unit. Source: TfL Quarterly Performance Report Q4 2024/25, Elizabeth line financial summary, page 13.

**Method.**

Direct comparison. No deflator. The 2019 forecast was stated in cash terms for 2024/25 as at 2019, and the TfL QPR outturn is reported in cash for the fiscal year. Both are cash figures and a real-terms restatement is not applied at this framing level (this is noted as a limitation in section 4).

```
drift_absolute = 652,000,000 − 1,037,000,000 = −385,000,000
drift_percent  = −385,000,000 / 1,037,000,000 × 100 = −37.1263%
```

**Yield decomposition.** The headline drift is decomposed into demand and yield components in the drift row's notes field as supporting analysis (not as a separate row). The 2019 TfL Business Plan's forecast demand for 2024/25 was 277 million journeys (quoted from source document notes for TFL-BUSINESS-PLAN-2019-12 in `data/sources.yaml`, not a loaded observation in its own right). The actual 2024/25 demand was 242,866,594 journeys per ORR-EL-JOURNEYS. This gives:

```
demand ratio        = 242,866,594 / 277,000,000 = 0.8768   (−12.32%)
yield forecast      = 1,037m / 277m = £3.744 per journey
yield actual        = 652m / 243m   = £2.685 per journey
yield ratio         = 2.685 / 3.744 = 0.7171               (−28.29%)
combined            = 0.8768 × 0.7171 = 0.6287
                    = 1 + drift_percent (reconciles exactly)
```

The −37.1% revenue drift therefore decomposes into approximately −12% demand (fewer journeys than the 2019 plan expected) and −28% yield (each journey generating materially less revenue than the 2019 plan expected). Most of the shortfall is yield per journey rather than journey volume.

**Decisions and alternatives considered.**

*Why the 2019 forecast rather than a later restated forecast.* TfL issued revised pre-opening and post-opening revenue forecasts in subsequent business plans, each reflecting updated assumptions about pandemic impact, phased opening, and fare policy. Using a restated forecast would answer a different question: "how well did the most recent pre-outturn forecast predict the outturn?" rather than "how much did the outturn deviate from the pre-pandemic baseline?" The 2019 forecast is the last clearly-pre-pandemic reference point and is therefore the one that makes the +21% demand finding (assumption 2) and the −37% revenue finding legible together. See the dual-baseline explanation below.

*Why decomposition in the notes rather than as separate rows.* The yield decomposition is supporting analysis. The demand forecast in the decomposition (277m) is not a loaded observation; it is a figure quoted from source document notes for the 2019 business plan. Storing the decomposition as separate drift rows would imply the same status as the directly-observed values (outturn passenger income and outturn journey counts), which would overstate the reproducibility of the decomposition. Keeping the decomposition in notes preserves the computation for readers who want it while being honest about its sourcing.

*Dual-baseline explanation for demand.* Assumption 2 compares 2024/25 outturn demand (242.9m) against the 2011 Crossrail Business Case steady-state forecast (200m), showing +21%. This revenue drift row compares outturn demand against the 2019 TfL Business Plan forecast (277m for 2024/25), showing −12%. Both are correct findings; they reflect the fact that between 2011 and 2019 TfL revised demand expectations upward as the line's opening approached, then the pandemic intervened before the outturn was realised. Any finding drafted from this investigation must name both baselines rather than present either in isolation. The drift row's notes carry this explanation in full.

**Output.**

One row in `crossrail_retrospective.drift_calculations`, linked to `assumption_key = revenue_2024_25`. `baseline_date = 2019-12-17` and `comparison_date = 2025-03-31`. No price-base adjustment applies, so the row uses the original dates.

**Confidence.** Medium. The arithmetic is exact. The direction (large negative drift, revenue below forecast) is robust. Three sources of uncertainty attach to the result.

First, a definitional match between "Passenger income" in the TfL QPR and the "passenger income" category in the 2019 Business Plan has not been independently verified. TfL may report Elizabeth Line revenue on several bases (gross, net of concession payments to the operator, net of franchise settlements). The exact basis of the 2019 forecast is not stated explicitly in publicly available materials. The drift row is flagged for definitional verification as part of the independent methodology review (see section 5.3). Until that verification is complete, the drift row is not suitable for citation in a published finding.

Second, the TfL QPR is unaudited quarterly reporting. Audited figures from TfL's 2024/25 Annual Report, when published, may revise the £652m figure. Revisions will be loaded as new append-only observation rows with a later `captured_at`, and any drift row affected will be re-run.

Third, the 2019 forecast is pre-pandemic. The pandemic intervened between forecast and outturn, affecting both demand (fewer journeys) and yield (lower average fare per journey, driven by travel pattern shifts toward off-peak and leisure). A no-pandemic counterfactual for either component is beyond the scope of this investigation.

### 3.4 Benefit-cost ratio, sensitivity restatement

**What is being scored.** The 2011 Crossrail transport-only benefit-cost ratio of 1.97 (DfT appraisal convention, national average salaries for time-saving valuation), against a sensitivity-only restatement using outturn cost and observed demand. The restatement is not a full NPV reconstruction, which would require TfL's internal appraisal model and is beyond the scope of a public-data investigation.

**Baseline.** 1.97, baseline date 2011-07-01, from `crossrail_retrospective.assumptions` (`assumption_key = benefit_cost_ratio_dft`). The figure is the transport-only BCR stated in the 2011 Crossrail Business Case Update Summary Report, confirmed in the NAO 2014 report. The equivalent wider-economic-benefit BCR was 3.09; TfL's transport-only BCR using London salaries for time-saving valuation was 2.55.

**Comparison.** No single comparison observation. The restated BCR is derived from the outputs of assumptions 1 and 2, combined with the baseline BCR, under a simple benefits-linear-in-demand assumption.

**Method.**

The restatement uses the standard sensitivity formula:

```
restated BCR = baseline BCR × (demand ratio / cost ratio)

where
  demand ratio = observed demand / forecast demand
  cost ratio   = observed cost / forecast cost
```

This formula holds benefits proportional to demand (a simplification: it assumes no non-linear network effects, no benefit re-estimation, no change in the mix of benefit categories) and it isolates the direction of BCR drift by treating cost drift and demand drift as independent multiplicative shocks. It is an order-of-magnitude calculation, not a full appraisal.

**Three co-equal scenarios** are computed under Scenario A (fix demand at the 2024/25 outturn). They differ only in how cost drift is expressed. Scenario B (a plausible long-run demand trajectory) is deferred; see section 5.2.

*Scenario A nominal cost ratio.* Uses the nominal cash cost ratio 18.8 / 14.8 = 1.2703. This matches the popular framing of Crossrail's cost performance (the +28% cash overrun cited in PAC-CROSSRAIL-2021) but mixes a 2010-11 priced baseline with a 2014-2020 cash outturn, conflating real-terms cost growth with construction-sector inflation.

```
demand ratio = 242,866,594 / 200,000,000 = 1.21433
cost ratio   = 18,800,000,000 / 14,800,000,000 = 1.27027
restated BCR = 1.97 × 1.21433 / 1.27027 = 1.883
drift_absolute = 1.883 − 1.97 = −0.087 (−4.40%)
```

*Scenario A real cost ratio, no pre-2014 correction.* Uses the real cost ratio derived from assumption 1 Row A (deflated outturn £18,463,709,875.03 / unadjusted baseline £14,800,000,000 = 1.2475). Internally consistent on price base to the extent that assumption 1 Row A is.

```
cost ratio   = 1.2475
restated BCR = 1.97 × 1.21433 / 1.2475 = 1.918
drift_absolute = 1.918 − 1.97 = −0.052 (−2.66%)
```

*Scenario A real cost ratio, 7.5% pre-2014 correction.* Uses the real cost ratio from assumption 1 Row B (deflated outturn £18,463,709,875.03 / pre-2014-adjusted baseline £15,910,000,000 = 1.1605). This is the methodologically cleanest version for a real-terms BCR: both sides of the cost ratio are in a single price base (January 2014 prices).

```
cost ratio   = 1.1605
restated BCR = 1.97 × 1.21433 / 1.1605 = 2.061
drift_absolute = 2.061 − 1.97 = +0.091 (+4.64%)
```

**Decisions and alternatives considered.**

*Why three co-equal scenarios rather than one.* The three cost-ratio treatments reflect three defensible methodological choices: nominal (matches popular framing), real with no pre-2014 correction (real but internally inconsistent with the baseline's price base), real with 7.5% pre-2014 correction (real and internally consistent to the best available approximation). Each answers a slightly different question. Reporting only one would privilege the question it answers over the others. The three-row structure lets a reader see the full range of defensible restatements and draw their own interpretation; it also documents the sensitivity of the BCR finding to the cost-treatment choice.

*Why no scenario is labelled "primary".* An earlier draft labelled the real-with-correction scenario as primary and the others as sensitivity. This framing was withdrawn because the 7.5% pre-2014 correction is an estimate at the middle of a 5-10% plausible range, and the band-change finding in assumption 5 flips depending on whether the correction is more or less than approximately 4.3%. Privileging any single scenario would overstate the methodological confidence the underlying data supports. All three scenarios are recorded as co-equal rows in `crossrail_retrospective.drift_calculations`, distinguished only by the cost-ratio methodology captured in each row's notes.

*Why linear benefits in demand.* The simplification holds benefits proportional to demand. In reality, benefit categories (time savings, reliability, wider economic benefits) scale through somewhat different functions of demand. A full appraisal would re-estimate each category; this investigation does not. The restated BCR is therefore order-of-magnitude. The direction of the drift is more robust than the precise magnitude.

*Why Scenario B is deferred.* Scenario B in `INVESTIGATION_BRIEF.md` section 6.4 specifies a "plausible long-run demand trajectory consistent with the first three years of operation". "Plausible trajectory" is a judgement call rather than a computation: candidates include linear extrapolation of the 2022/23-2024/25 growth rate, logistic fitting to an assumed peak, or matching to comparable line openings. The choice has its own methodological weight and warrants separate framing. Deferred to a follow-up session; see section 5.2.

**Output.**

Three rows in `crossrail_retrospective.drift_calculations`, linked to `assumption_key = benefit_cost_ratio_dft`, with `series_id = NULL` (compound calculation, no single external series). Restated BCR range across the three rows is 1.88 to 2.06. Each row's notes field identifies the cost-ratio methodology applied and cross-references assumption 1's parent drift row where applicable.

**Confidence.** Low. Three reasons. First, the benefits-linear-in-demand assumption is a strong simplification; a full NPV reconstruction would likely produce somewhat different numbers. Second, the three co-equal scenarios span a range that straddles the medium/high value-for-money boundary (see assumption 5), meaning the qualitative finding depends on methodological choices within the 5-10% pre-2014 correction range. Third, caveats 1 and 2 both apply: the real cost ratio depends on the ONS-OPI vs BCIS-TPI choice, and the demand ratio conflates pre-pandemic trend drift with post-pandemic recovery.

### 3.5 Value-for-money band

**What is being scored.** The DfT value-for-money band into which the 2011 Crossrail BCR placed the programme (band 2, "medium", BCR range 1.5 to 2.0), against the restated band implied by each of the three assumption-4 BCR scenarios.

**Baseline.** Band code 2 (medium), baseline date 2011-07-01, from `crossrail_retrospective.assumptions` (`assumption_key = value_for_money_band`). The band encoding is integer-valued: 1 = poor (BCR < 1.5), 2 = medium (1.5 to 2.0), 3 = high (2.0 to 4.0), 4 = very high (> 4.0). The thresholds follow DfT Transport Analysis Guidance (TAG).

**Comparison.** For each of the three restated BCR rows in assumption 4, the band implied by the restated BCR value is looked up against the TAG thresholds:

```
Scenario A nominal:                          BCR 1.883 → band 2
Scenario A real, no pre-2014 correction:     BCR 1.918 → band 2
Scenario A real, 7.5% pre-2014 correction:   BCR 2.061 → band 3
```

**Method.**

A discrete lookup from continuous BCR to integer band code, computed for each assumption-4 scenario and stored as its own drift row to maintain one-to-one parity with assumption 4.

```
Row 5a (from BCR 1.883):  restated band 2; drift_absolute  0; drift_percent  0.00%
Row 5b (from BCR 1.918):  restated band 2; drift_absolute  0; drift_percent  0.00%
Row 5c (from BCR 2.061):  restated band 3; drift_absolute +1; drift_percent 50.00%
```

**Decisions and alternatives considered.**

*Why three rows rather than an aggregated two.* Two of the three BCR scenarios produce the same band outcome (band 2, no change). An aggregated presentation would collapse these into a single row with a note that it represents two scenarios. The three-row structure is preserved instead: it maintains one-to-one parity with assumption 4 (each BCR scenario maps to exactly one band row), it makes the outcome distribution explicit to a reader scanning the table (two of three scenarios at band 2, one at band 3), and it supports clean extension if Scenario B is added in a future iteration. The apparent duplication of the band 2 outcome is honest rather than redundant: two distinct methodological choices happen to produce the same categorical result.

*Why drift_percent is ordinal on this assumption.* The `drift_percent` column is mechanically computed as (comparison − baseline) / baseline × 100 for every row in `crossrail_retrospective.drift_calculations`, regardless of the underlying unit. For row 5c, this gives (3 − 2) / 2 × 100 = 50%. This is arithmetically correct but conceptually misleading if read as a continuous drift metric. A 50% band drift does not mean 50% more value for money; it means one band-position movement on a four-band scale. Each assumption-5 row carries this clarification in its notes field. Any reader interpreting drift_percent on these rows must check the assumption's unit (`band_code`) and consult the parent assumption-4 row for the continuous BCR drift.

*How row 5c's band change is framed.* Row 5c is the only row of the three that produces a band change (medium to high). The change is sensitivity-dependent: it holds under the 5-10% plausible range of pre-2014 corrections (the BCR sits just above 2.0 in this range), but it flips if no pre-2014 correction is applied (row 5b, BCR 1.918, stays in band 2). The boundary at which the restated BCR crosses 2.0 corresponds to a cumulative pre-2014 correction of approximately 4.3%. Row 5c's notes flag this explicitly and state: "Findings drafted from this row must describe the band change as methodologically sensitive rather than robust." The defensible finding for publication is not "Crossrail's VFM band drifted from medium to high" but "The restated BCR sits close to the medium/high boundary, with sensitivity-dependent band assignment across the three co-equal scenarios."

**Output.**

Three rows in `crossrail_retrospective.drift_calculations`, linked to `assumption_key = value_for_money_band`, with `series_id = NULL`. Each row cross-references its parent BCR row in notes with an inline SQL query pattern, so that the derivation chain is self-traceable: a reader looking at any assumption-5 row can jump to the parent BCR row with one query, without rebuilding the join against assumption 4.

**Confidence.** Low across all three rows, inherited from the parent BCR rows in assumption 4. Row 5c carries an additional sensitivity caveat because the band change it records depends on a methodological choice within a narrow window (4.3% pre-2014 correction boundary).

**What this tells us.** Categorical findings have a different epistemic status than continuous findings. When a categorical claim depends on a continuous metric crossing an externally defined threshold, the strength of the claim is bounded by the sensitivity of the continuous metric at the threshold. For Crossrail's BCR restatement, one of three co-equal scenarios crosses the 2.0 medium/high threshold by only 0.06 points; the other two scenarios fall below the threshold by 0.08 and 0.12 points respectively. Any analysis that reports a band change as a headline when the underlying continuous metric sits within a band-width of a boundary is overclaiming. More generally: drift analyses that map continuous metrics through discrete banding frameworks (VFM bands, credit ratings, regulatory thresholds) should report the continuous drift as the primary finding, with the categorical consequence flagged as secondary and sensitivity-dependent rather than as a headline.

## 4. Caveats in operational form

The three methodological caveats from `INVESTIGATION_BRIEF.md` are restated here in their operational form, specifying which calculations they affect and how.

### 4.1 Caveat 1: Construction cost index choice

The canonical rail construction cost index is the BCIS Tender Price Index, produced by the Royal Institution of Chartered Surveyors. BCIS is subscription-restricted and cannot be loaded into a public investigation. The primary reprice basis for this investigation is the free public ONS Construction Output Price Index (Infrastructure new work), which measures output prices rather than tender prices and uses a different compositional weighting.

The caveat affects two calculations:

- **Assumption 1 (construction cost).** The deflator applied to the £18.8bn outturn uses ONS-OPI-INFRA-NEW. A BCIS-based reprice would produce a different magnitude of real-terms residual. Whether a BCIS-based reprice would also change the direction of the finding is not independently established by this investigation; a future iteration that loads BCIS would answer this question directly.
- **Assumption 4 scenarios using the real cost ratio.** Both the no-correction and 7.5%-corrected real cost ratios are derived from the assumption 1 deflator. They inherit caveat 1 by construction.

The Scenario A nominal cost ratio in assumption 4 does not apply a deflator and therefore does not inherit caveat 1. This is one reason the three assumption-4 scenarios span a wider range than they otherwise would: the nominal scenario sits further from the two real scenarios precisely because of the index uncertainty that caveat 1 describes.

Where a public BCIS reference point is available (typically via a cited NAO or IPA report that quotes a BCIS value), it would be referenced for comparison. No such reference point is currently loaded in this investigation. A future iteration that gains access to BCIS would recompute the assumption 1 rows using BCIS-TPI as the deflator; the results would be stored as additional append-only rows rather than as replacements.

### 4.2 Caveat 2: Pandemic as break in the demand series

The 2011 passenger forecast was constructed without a pandemic in its baseline assumptions. The outturn observed in 2024/25 captures both pre-pandemic trend drift (what demand might have been if the programme had delivered on its 2011 timetable and no pandemic had occurred) and post-pandemic recovery dynamics. Attributing the full variance between forecast and outturn to either cause alone would mislead.

The caveat affects three calculations:

- **Assumption 2 (passenger demand).** The +21.4% headline drift conflates the two components. Proper decomposition requires a London rail proxy series covering 2011-2019 to estimate the no-pandemic counterfactual. No such proxy is loaded. The decomposition is deferred; see section 5.1. The published headline is therefore a lower bound on real drift rather than a decomposed estimate.
- **Assumption 3 (revenue).** The demand ratio used in the yield decomposition (0.8768, based on forecast 277m vs observed 243m) also conflates the two components. The decomposition is reported because the yield split is methodologically informative even without the decomposition, but the 12% demand shortfall against the 2019 forecast should be read as a pandemic-adjusted residual rather than a structural underperformance.
- **Assumption 4 (BCR).** The demand ratio in the BCR formula is the same as assumption 2's. The restated BCR inherits the caveat, though the BCR's direction of drift is more robust to the decomposition question than its magnitude.

The caveat is not a flaw in the calculation. It is a real property of the forecast-vs-outturn comparison for any programme whose baseline preceded an exogenous shock of the pandemic's magnitude. The methodology chooses to report the headline with the decomposition flagged as deferred, rather than to defer the publication of the headline itself. A reader who wants the decomposition can read section 5.1 for the unblocking requirement.

### 4.3 Caveat 3: Multiple restated business cases

The 2011 Crossrail Business Case was informally updated multiple times as funding increases were announced (notably in 2018, 2019, and 2020), but no comprehensive restated BCR with full methodology was ever published. This investigation therefore compares the 2011 published baselines to 2024/25 outturn, not to a sequence of restated BCRs that might have shown "what the sponsors thought was happening at each decision point".

The caveat affects all five assumptions:

- **Assumptions 1, 2, 3, 4, 5** all take their baselines from published 2011 business case figures (or, for assumption 3, the 2019 TfL Business Plan, which is the last clearly pre-pandemic published forecast). No intermediate restated figures are used as comparison baselines.

The implication for findings drafting is that the investigation is not measuring "how well did the sponsors forecast" in the sense of "were they right each time they re-forecast". It is measuring "how did the 2011 published claims compare to the eventual outturn" (with 2019 substituted for the revenue claim because 2011 did not specify a 2024/25 revenue). Any commentary on sponsor forecasting quality is bounded by this definition. The investigation cannot, for example, say that "TfL's 2019 forecast was more accurate than its 2011 forecast" because the two forecasts are of different things (the 2011 forecast did not specify 2024/25 revenue; the 2019 forecast did not specify steady-state demand).



## 5. Known limitations and deferred work

Three pieces of work are explicitly deferred and flagged for future iterations of this investigation.

### 5.1 Caveat 2 decomposition for assumption 2

Assumption 2 (passenger demand) is scored as a headline drift: +21.4% of outturn over the 2011 "steady-state" forecast of 200 million. The 2011 forecast predates the pandemic, and a proper attribution of the +21.4% between pre-pandemic trend drift and post-pandemic recovery dynamics requires a London rail proxy series covering 2011 to 2019 (the Elizabeth Line itself did not exist before May 2022). No such proxy series is currently loaded in `pda_shared.external_observations`. The decomposition is deferred to a follow-up unit of work that would load the proxy, compute the 2011-2019 trend, project it to a no-pandemic 2024/25 counterfactual, and decompose the observed drift against it. The headline drift row is published with this limitation clearly stated in its notes field.

### 5.2 Scenario B for assumption 4

Assumption 4 (restated BCR) is scored under Scenario A only: hold demand at the 2024/25 outturn. Scenario B in `INVESTIGATION_BRIEF.md` section 6.4 specifies a restatement under "a plausible long-run demand trajectory consistent with the first three years of operation". Implementing Scenario B requires an explicit methodology for "plausible long-run trajectory", which is a judgement call rather than a computation. Candidate approaches include linear extrapolation of the 2022/23-2024/25 growth rate, logistic fitting to an assumed peak, or matching to comparable line openings such as the Jubilee Line extension. The choice itself has methodological implications that warrant a separate review. Deferred.

### 5.3 Definitional verification on revenue

Assumption 3 (2024/25 revenue) uses TfL Quarterly Performance Report "Passenger income" as the comparison value (£652m for 2024/25). The 2019 TfL Business Plan forecast of £1,037m for 2024/25 uses the same general category of "passenger income", but a precise definitional match between the two figures (gross, net of concessions, net of franchise payments) has not been independently verified. The drift row is flagged as requiring definitional verification before any finding is drafted. The verification rides with Laura's methodology review.

### 5.4 Methodological correction made during analysis

Section 6.1 of `INVESTIGATION_BRIEF.md` originally specified a one-sided reprice method for assumption 1: reprice the £14.8bn baseline to current prices, compare against cash outturn. Implementing this during the drift calculations session produced a result whose direction depended on the reprice target date rather than on any underlying fiscal fact. The method was corrected to express both sides of the comparison in the same price base by deflating the outturn rather than repricing the baseline. The corrected method is now in `INVESTIGATION_BRIEF.md` section 6.1; the full reasoning for the correction is in the Cross-cutting decisions section of `analysis/drift-decisions-log.md`. The correction affects assumption 1 directly and assumption 4's real-cost scenarios by inheritance. A reader comparing this investigation to an earlier draft, or to a future PDA Investigations case, will find the correction recorded in both places.

## 6. Review and reproducibility

### 6.1 Independent review

The methodology of this investigation, and the drift calculations produced from it, will be independently reviewed before publication of any finding. The reviewer is an independent domain expert in public-sector programme assurance who has elected to remain anonymous. The review is structured as approximately 45 minutes of the reviewer's time covering the five assumptions, the method applied to each, the three caveats, and the identified limitations.

Reviewer metadata is held in `pda_shared.reviewers` (service-role access only). The review itself is recorded in `pda_shared.reviews` with `consent_to_name = false`. Feedback that changes the analysis is recorded and reflected in the published methodology. A sceptical or negative review is published alongside any finding, not hidden from it.

Publication of any finding in `crossrail_retrospective.findings` is gated on the presence of an approved review in `pda_shared.reviews`. This is enforced by the investigation's publication workflow, not by a database constraint.

### 6.2 Reproducibility

Every calculation in this methodology is reproducible from public inputs. The steps are:

1. Clone the repository at `github.com/antnewman/crossrail-retrospective-2026`.
2. Connect to the investigation's Supabase project (ID `bulheatuxvktopxrwbvs`, read-only access to the public schemas).
3. Load the observations from `data/observations/` or query `pda_shared.external_observations` directly.
4. Apply the methods specified in section 3 to reproduce each drift row.

The observation loading process is documented in the ingest history on the `data/ingest-*` branches of the repository. Individual observations are traceable through their notes fields to primary sources (ONS, ORR, BoE, TfL QPRs). The Supabase schema is append-only: a reader inspecting the database in six months sees exactly the same rows that underpin any finding published now.

### 6.3 What a reader can check

Anyone who wishes to audit this investigation can:

- Verify that each drift row's baseline and comparison values match the sources cited in their notes fields.
- Reproduce the arithmetic of each drift calculation from the observations.
- Query observations and drift calculations directly against Supabase.
- Confirm that the method specified in this document matches what was executed, by comparison against `analysis/drift-decisions-log.md`.
- Identify where the method departs from the original brief, and why, through the cross-cutting decisions entry in the decisions log and section 5.4 of this document.

The intent is that no reader needs to trust the author's summaries: every step is legible from public sources.
