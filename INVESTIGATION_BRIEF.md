# Investigation brief: a retrospective drift analysis of the Crossrail business case

**Working title:** *Before and after: what the Crossrail business case got
right, got wrong, and what that tells us about assumption drift on major
programmes.*

**Author:** Ant Newman, TortoiseAI.
**Affiliation:** TortoiseAI (tortoiseai.co.uk). ORCID 0000-0002-8612-3647.
**Status:** In progress (April 2026). Target publication: end May 2026.
**Licence:** CC BY 4.0 (written content), MIT (code and data).

## Investigation question

The Crossrail programme published a formal business case in 2011. It
committed to specific numerical claims: a £14.8bn funding envelope, a
benefit-cost ratio of 1.97 transport-only (3.09 with wider economic
benefits), approximately 200 million annual passenger journeys at full
opening. The Elizabeth Line has now been open since May 2022 and full
services run since 2023.

Thirteen years after the baseline, do the original assumptions hold when
scored against what actually happened? What was right, what was wrong, and
what does the pattern tell us about how assumption drift moves on major
infrastructure programmes over time?

## Why Crossrail, and why retrospective

The PDA Investigations programme will publish a sequence of drift analyses
on UK major programmes. The first case is deliberately retrospective. A
retrospective case teaches the method by showing both directions of drift
(cost and demand) on outcomes that readers can verify from the published
record. It demonstrates that the tool produces defensible findings before
the tool is applied to a live case.

A retrospective case also avoids the political and methodological
complications of analysing a live programme. The Elizabeth Line is open and
operating. The overrun is settled history. The twin-drift finding, cost up
and demand up, is available to anyone who reads the public record and does
the arithmetic. The contribution of this investigation is the tooling, the
data model, and the reproducibility, not the underlying facts.

## Anchor

Unlike some subsequent cases in this programme, this investigation does not
operationalise a specific parliamentary recommendation. Instead, the anchor
is the published 2011 Crossrail Business Case Update Summary Report, which
committed to specific numerical claims, and the subsequent National Audit
Office reports (2014, 2019, 2021) and Committee of Public Accounts reports
(2014, 2021) that tracked progress against those claims.

The investigation applies a retrospective validation method of a kind that
NAO performs routinely on a multi-year lag. What is new here is not the
exercise of comparing baseline to outturn, but that the method is run
against public data, by an open-source tool, in days rather than months,
fully reproducibly.

## The five assumptions

All five are held in `data/assumptions.yaml` and loaded into the
`crossrail_retrospective.assumptions` table. They are listed here with
their baseline values and primary sources; the YAML file carries the full
detail.

### Primary assumption

1. **Construction cost: £14.8bn original funding envelope (2010-2011
   prices).** Source: Crossrail Business Case Update Summary Report, July
   2011. The funding envelope that the sponsors (Department for Transport
   and Transport for London) committed to at the 2011 revision of the
   business case.

### Supporting assumptions

2. **Annual passenger journeys at full opening: approximately 200
   million.** Source: 2011 business case, cited in NAO 2014 report and
   subsequent Commons Library research briefings.

3. **Annual fare revenue at steady state: over £1bn by 2024-25.** Source:
   TfL Crossrail business plan, published January 2020 (the most detailed
   published pre-pandemic revenue forecast).

4. **Benefit-cost ratio (transport-only, DfT value): 1.97.** Source: 2011
   business case, confirmed by NAO 2014 report. Wider-economic-benefit
   BCR stated as 3.09; TfL's equivalent transport-only BCR (using London
   salaries) stated as 2.55.

### Downstream result

5. **Value for money band: DfT "medium" (1.5 to 2.0).** Source: 2011
   business case, NAO 2014 report, DfT appraisal guidance. The band
   within which the original transport-only BCR fell, and the band
   against which the retrospective result will be compared.

## External data sources

All public. Full detail in `data/external_series.yaml`.

**For the construction cost reprice:**
- **ONS Construction Output Price Index, Infrastructure (new work).**
  Public and free. The primary reprice basis for this investigation.
- **BCIS Tender Price Index.** The industry-canonical rail construction
  inflation series. Subscription-restricted. Referenced in the methodology
  as a comparison point where a public data point is available, but not
  the primary reprice basis. See caveat 1.

**For the passenger demand cross-check:**
- **ORR Passenger Rail Usage statistics, Elizabeth Line series.** Public,
  quarterly and annual data from May 2022 onwards.
- **TfL Elizabeth Line Committee papers.** Publicly available via the TfL
  website.

**For the revenue trajectory cross-check:**
- **TfL Quarterly Progress Reports and Annual Reports.** Public.
- **London Assembly research publications on Elizabeth Line performance.**
  Public.

**For the BCR restatement:**
- **DfT appraisal guidance (TAG).** Public, for the value-for-money bands
  and methodology.
- **Bank of England Bank Rate.** Public, for discount rate sensitivity.

## Method

The method is a series of scoring steps, one per assumption. Each step
produces a row in `crossrail_retrospective.drift_calculations` that records
the inputs, the formula applied, the result, and the caveat flags.
Calculations are idempotent: given the same inputs, re-running them
produces the same row.

Detailed method will be set out in `methodology.md` at repository root,
with section numbers corresponding to each assumption. High level:

**1. Construction cost reprice (primary).** The £14.8bn envelope in
2010-2011 prices is repriced to a current-price equivalent using the ONS
Construction OPI (Infrastructure) from the baseline year to 2025. This
gives an "if nothing else had changed" comparison point. The actual
outturn (approximately £18.8bn by 2020, with subsequent minor additions)
is then compared to the repriced baseline. The difference between repriced
baseline and outturn is the portion of the overrun that cannot be
attributed to construction sector inflation.

**2. Passenger demand comparison.** The 200 million annual journey
assumption is compared to the actual ORR figure for 2024-25 (242.9
million). The comparison separates pre-pandemic trend (2022-2023 ramp-up)
from post-pandemic recovery (2023-2025), because the 2011 forecast did not
contemplate a pandemic and attributing the full variance to either cause
would mislead. See caveat 2.

**3. Revenue trajectory comparison.** The over-£1bn by 2024-25 revenue
forecast from the January 2020 TfL plan is compared to the actual figure
for 2024-25 (approximately £606m in 2023-24, latest publicly available
at time of analysis). The comparison uses only publicly-published TfL
revenue numbers.

**4. BCR restatement (sensitivity).** The 1.97 BCR is restated under two
scenarios. Scenario A: use outturn cost and 2024-25 passenger demand
held at steady state. Scenario B: use outturn cost and a plausible
long-run demand trajectory consistent with the first three years of
operation. The sensitivity result is not a full NPV reconstruction
(that is beyond the scope of a public-data investigation and would
require TfL's internal appraisal model). It is an order-of-magnitude
estimate of the direction and rough scale of the drift in the BCR.

**5. Value-for-money band check.** Under the restated BCR scenarios,
does the programme still fall within DfT's "medium" VFM band, or has
it drifted into a different band?

## Three methodological caveats

Every published output discloses these three caveats in full.

### Caveat 1: Construction cost index choice

The canonical index for rail construction cost inflation is BCIS Tender
Price Index (TPI), produced by the Royal Institution of Chartered
Surveyors. BCIS is subscription-restricted. The ONS Construction Output
Price Index (Infrastructure subset) is the free public alternative but
measures a slightly different quantity (output prices rather than tender
prices), with a different compositional weighting.

This investigation uses ONS Construction OPI as the primary reprice
basis, for reproducibility by any reader. The methodology acknowledges
that a BCIS-based reprice would produce a slightly different numerical
finding. Where a public BCIS reference point is available (for example,
through cited NAO or IPA reports that quote BCIS), it is noted for
comparison. The direction of the finding is robust to the index choice;
the magnitude is not.

### Caveat 2: Pandemic as break in the demand series

The 2011 passenger forecast was constructed without a pandemic in its
baseline. Comparing 2024-25 outturn against the 2011 forecast in a
single number would mis-attribute variance to causes that the forecast
could not have anticipated. The analysis therefore separates
pre-pandemic trend drift (2011 to 2019, using comparable London rail
proxies since the Elizabeth Line did not exist until 2022) from
post-pandemic recovery drift (2020 to 2025, using the Elizabeth Line
directly). Both are reported; the reader can reconstruct a combined
view from the disclosed components.

### Caveat 3: Multiple restated business cases

The 2011 business case was informally updated multiple times as funding
increases were announced (notably 2018, 2019, 2020), but no
comprehensive restated BCR with full methodology was ever published.
This investigation therefore compares the 2011 published baselines to
2024-25 outturn, not to a sequence of restated BCRs. This is a real
limitation: we cannot reconstruct how the sponsors revised their own
view at each funding decision, because they did not publish a revised
BCR at each step. The method compares "what 2011 committed to" with
"what actually happened", not "what 2018 or 2019 thought was happening
at the time."

## Data model and reproducibility

Data is stored in Supabase project `pda-investigations`
(ID `bulheatuxvktopxrwbvs`, eu-west-2 London region, free tier).

- `pda_shared.source_documents`: primary source metadata, keyed by
  `citation_key`. Shared across all investigations.
- `pda_shared.external_series`: external data series metadata. Shared.
- `pda_shared.external_observations`: append-only time-series
  observations. Shared.
- `crossrail_retrospective.assumptions`: the five assumptions, with
  `is_superseded` flag (unused here; assumptions were not revised in the
  sources we use).
- `crossrail_retrospective.drift_calculations`: scored outputs, one row
  per assumption per calculation run.
- `crossrail_retrospective.findings`: narrative findings, public only
  when `published = true` and an approved review exists in
  `pda_shared.reviews`.

All tables are append-only. Every claim is reproducible from publicly
available inputs. If an input is not public, it cannot be used in a
published finding.

## Tooling

Analysis runs through the [PDA Platform](https://github.com/antnewman/pda-platform),
the same open-source Model Context Protocol platform used across the PDA
Investigations programme. Code specific to this investigation lives in
[`analysis/`](analysis/). The analysis is deterministic given the inputs.
Each run stamps the inputs, the platform version, and a checksum into
the result row, so that any reader can reproduce the scored output from
the same inputs.

## Review and attribution

Independent review is a prerequisite for publication of findings from
this investigation, consistent with the umbrella methodology described
in `../pda-investigations/methodology-shared.md`.

For this investigation, the methodology will be reviewed by an
independent domain expert in public-sector programme assurance. The
reviewer has elected to remain anonymous. The review will follow a
structured methodology review format: approximately 45 minutes of the
reviewer's time, covering the five assumptions, the method for each, and
the three caveats. The reviewer's identity, credentials, and affiliation
are held privately in the Supabase `pda_shared.reviewers` table, which
is service-role only. The review itself is recorded in
`pda_shared.reviews` with `consent_to_name = false`.

The published methodology, when it carries findings, will describe the
review in the form: "The methodology was independently reviewed in
[month] 2026 by a domain expert in public-sector programme assurance.
The reviewer has elected to remain anonymous; the review is recorded
privately in the investigation's database." This is standard practice
in peer-reviewed contexts. It preserves the integrity of the review
commitment without disclosing the reviewer's identity.

If the reviewer's substantive feedback changes the analysis materially,
that change is recorded and reflected in the published methodology. A
negative or sceptical review is published alongside the finding, not
hidden from it.

## Publication and update policy

The primary artefact is a full analytical report on the Tortoise website,
with the Supabase schema, data, and analysis code linked from it. A
Zenodo release with DOI is made at publication. Derivative formats
(short-form, LinkedIn, summary) carry the same methodological caveats.

Findings that are boring are published. Findings that contradict
expected framing are published with equal prominence to those that do
not. The framing can emphasise what is interesting; it cannot hide what
is inconvenient.

If TfL, DfT, or the NAO publishes a new report on Elizabeth Line
outturn between now and publication, the analysis is re-run against
the new information and the report is revised before release. If a new
edition of an external series publishes after release, a follow-up
note is appended; the original report is not silently modified.

## Scope, explicitly stated

This investigation is a demonstration of retrospective drift analysis on
a completed major programme. It is not:

- A criticism of the Crossrail sponsors, the Department for Transport,
  Transport for London, Crossrail Ltd, or any individual
- A claim that the tool can replace NAO, NISTA, or DfT assurance
- A policy recommendation about future major rail programmes
- A comparison to Crossrail 2 or to HS2

It is a specific, bounded exercise: taking the 2011 published
assumptions, scoring them against current public data, and reporting
the direction and approximate magnitude of the drift, with the method
fully disclosed.

## Contacts

Author: Ant Newman, TortoiseAI. ORCID
[0000-0002-8612-3647](https://orcid.org/0000-0002-8612-3647).

Correspondence on the methodology is welcome as issues on this
repository.