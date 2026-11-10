# Scenario brief — Essay 001 (owner-confirmed)

This brief defines a small, transparent **exploration** confined to 16 to 19 October 1813. It is not a simulation of the battle and not a prediction. Anything bigger belongs in a follow-up essay (risk R-02).

The scenarios below were proposed by the assistant that drafted this brief, building on the cavalry theme in your user stories. **Edit, replace or delete anything.** Every number marked *proposed* is an arbitrary starting point and an assumption, not a sourced fact. When you have read and edited everything, change the next line to `CONFIRMED: yes`. The agent will not run P-026 until you do.

CONFIRMED: no

## What the model does
Daily bookkeeping for two sides over four days (16, 17, 18, 19 October): starting strength, minus losses, plus documented arrivals. Starting strengths and total losses are **sampled from the ranges in `data/input/figures.csv`** (so source disagreement becomes uncertainty, not a single number). Daily shares of the total losses and the scenario parameters below are explicit assumptions. There is **no combat resolution and no terrain**. It explores how source uncertainty and two specific changes alter relative strength over the four days.

Output per scenario, per day, per side: the 10th, 50th and 90th percentile of effective strength and of cavalry strength (from a fixed-seed Monte Carlo of 1,000 draws).

## Scenarios
### S0 historical (baseline)
All parameters at their documented values.

### S1 cavalry parity (the owner's theme)
Question: how different does the French side's strength look if its cavalry shortfall were smaller?
Parameter `french_cavalry_multiplier`: *proposed* uniform 1.0 to 1.5, applied to the French side's starting cavalry.

### S2 delayed northern army (proposed by the assistant)
Question: how does the balance over the four days change if the coalition's northern army arrived later?
Parameter `northern_army_delay_days`: *proposed* integer 0, 1 or 2, shifting that army's arrival.

## Assumptions the agent must state in the export
- Daily share of total losses, per day: *proposed* 16 Oct 0.35, 17 Oct 0.05, 18 Oct 0.45, 19 Oct 0.15 (arbitrary; adjust to your reading of the sources).
- Seed: fixed constant in code; draws: 1,000.
- Arrivals and any other facts the model uses must come from `research.md` with source ids. If a needed figure is missing, stop and report; do not fill the gap.

## Limitations the agent must state in the export (add your own)
- Not a simulation of fighting; no terrain, morale, leadership, or timing within a day.
- Ranges come from sources that disagree; candidate rows are unverified.
- Daily loss shares and scenario parameters are the author's assumptions.
- Results show relative strength under assumptions, not what would have happened.
