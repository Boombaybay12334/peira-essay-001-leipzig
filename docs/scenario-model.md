# Scenario model

This is a small uncertainty exploration under stated assumptions, not a battle
simulation. Each scenario uses 1,000 draws from a dedicated
`random.Random` instance. Starting strengths, total losses, cavalry strengths,
and documented arrivals are sampled uniformly from the candidate ranges below.

| Quantity | Figure row | Source IDs |
|---|---|---|
| French starting strength | Forces concentrated near Leipzig before the battle | WHE |
| Coalition starting strength | Forces approaching Leipzig | WHE |
| French total losses | French casualties during the battle | WHE, HISTORY |
| Coalition total losses | Coalition casualties | WHE, HISTORY |
| French cavalry starting strength | French cavalry at Leipzig | WIKI-FR-OOB |
| Coalition cavalry starting strength | Coalition cavalry at Leipzig | WIKI-FR-COAL |
| Coalition reinforcements on 17 October | Allied reinforcements arriving on 17 October | WHE |
| French reinforcements on 17 October | French reinforcements arriving on 17 October | WHE |
| Army of the North component | Army of the North at Leipzig | NAP-SERIES-NORTH |

The Army of the North is treated as a component of the documented coalition
reinforcement arrival, so S2 delays that component rather than counting it
twice. Its arrival is documented by `HISTORYOFWAR-17OCT`. Places and dates are
limited to timeline rows with source-backed coordinates on 16–19 October 1813.

For each day and side, effective strength and cavalry strength are calculated
as starting value minus cumulative loss share times total losses, plus arrivals
present. Outputs report p10, p50, and p90, rounded to three decimals.
