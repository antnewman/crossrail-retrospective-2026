# Crossrail retrospective drift analysis

**Working title:** *Before and after: what the Crossrail business case got right, got wrong, and what that tells us about assumption drift on major programmes.*

**Part of:** [PDA Investigations](https://github.com/antnewman/pda-investigations)
**Tool:** [PDA Platform](https://github.com/antnewman/pda-platform)
**Related case:** [MTD Assumption Drift 2026](https://github.com/antnewman/mtd-assumption-drift-2026) (paused, to be resumed after publication of this case).
**Author:** Ant Newman, TortoiseAI. ORCID: [0000-0002-8612-3647](https://orcid.org/0000-0002-8612-3647).
**Status:** In progress (April 2026). Target publication: end May 2026.
**Licence:** [CC BY 4.0](LICENCES/CC-BY-4.0.txt) for written content, [MIT](LICENCES/MIT.txt) for code and data.

---

## The question

The Crossrail programme published a formal business case in 2011 committing to specific numerical claims: a £14.8bn funding envelope, a benefit-cost ratio of 1.97 (transport-only), approximately 200 million annual passenger journeys at full opening. The Elizabeth Line has now been open since May 2022. Thirteen years after the baseline, do the original assumptions hold when scored against what actually happened?

## Why retrospective, as the first case

The PDA Investigations programme publishes a sequence of drift analyses on UK major programmes. The first case is deliberately retrospective. A retrospective case teaches the method by showing both directions of drift (cost and demand) on outcomes that readers can verify from the published record. It demonstrates that the tool produces defensible findings before it is applied to a live case.

## Method in one paragraph

Five published assumptions in [`data/assumptions.yaml`](data/assumptions.yaml) (construction cost envelope, annual passenger demand, fare revenue trajectory, benefit-cost ratio, value-for-money band) are scored against public external series in [`data/external_series.yaml`](data/external_series.yaml) (ONS Construction Output Price Index, ORR passenger rail usage statistics, TfL quarterly reports, DfT appraisal guidance, Bank of England Bank Rate). All sources carry citation keys into [`data/sources.yaml`](data/sources.yaml). Calculations run through the open-source [PDA Platform](https://github.com/antnewman/pda-platform). Results are appended to a Supabase database and published alongside the methodology.

## Repository layout

- [`INVESTIGATION_BRIEF.md`](INVESTIGATION_BRIEF.md): the case-specific framing, decisions, and investigated assumptions.
- [`methodology.md`](methodology.md): the public-facing methodology document.
- [`data/`](data/): structured inputs. Sources, external series, assumptions.
- `analysis/`: analysis scripts and notebooks.
- `findings/`: findings output. Tables, charts, narrative drafts.
- `sources/`: archived copies of primary sources where licensing permits.
- [`AGENT_CONTEXT.md`](AGENT_CONTEXT.md): standing context for AI coding assistants, shared across PDA Investigations.

## Methodological caveats

Every output of this investigation discloses these caveats.

1. **Construction cost index choice.** The investigation uses the free public ONS Construction Output Price Index (Infrastructure) as the primary reprice basis, for reproducibility by any reader. The industry-canonical BCIS Tender Price Index is subscription-restricted and is referenced only where a public comparison point is available. The direction of the finding is robust to the index choice; the magnitude is not.
2. **Pandemic as a break in the demand series.** The 2011 passenger forecast was constructed without a pandemic in its baseline. The analysis separates pre-pandemic trend drift from post-pandemic recovery drift, so that variance is not mis-attributed to causes the forecast could not have anticipated.
3. **Multiple restated business cases.** The 2011 business case was informally updated as funding increases were announced, but no comprehensive restated BCR with full methodology was ever published. The investigation compares the 2011 published baselines to 2024-25 outturn, not to a sequence of restated BCRs.

## Reproducibility and review

Every claim is reproducible from public inputs. Assumption values, external observations, and drift calculations are append-only; historical state stays queryable. Findings require independent domain review, recorded in the `reviews` table, before any publication.

## Citing this investigation

See [`CITATION.cff`](CITATION.cff). A Zenodo DOI is issued on publication.

## Licence

Written content is released under [CC BY 4.0](LICENCES/CC-BY-4.0.txt). Code and structured data are released under [MIT](LICENCES/MIT.txt). See [`LICENCE`](LICENCE) for the combined notice.
