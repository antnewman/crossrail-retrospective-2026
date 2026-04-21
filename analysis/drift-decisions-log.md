# Drift calculations: decisions log

Session date: 2026-04-21
Session purpose: capture methodological decisions made during Crossrail drift calculations, for use in writing methodology.md.

This log is updated in real time during the drift calculations session. Each entry records a decision, the alternatives considered, and the reasoning for the choice made.

## Assumption 1: construction_funding_envelope

[populated during session]

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
