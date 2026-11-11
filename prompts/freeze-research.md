# Freeze the research repo and write its state document

You are in the repository `peira-essay-001-leipzig`. Read `AGENTS.md`.

**How to work (any agent, including Antigravity):** use Planning mode, show the plan first and **wait for the owner's approval before changing anything**. **Workspace boundary:** do not read or write any path outside this repository. After approval, no more questions unless a stop condition applies.

**MERGE POLICY:** one branch, PR, CI green, squash-merge, delete branch.

**Freeze means no change to model behaviour, inputs, or exports.** You may fix docs and remove verified-dead files.

## 1. Preflight (read-only)
Print pass/fail for: on `main`, up to date, clean tree; `uv sync --frozen && uv run pytest` green; `uv run export` and `uv run export-scenarios` leave `git diff --exit-code exports/` clean. Record the baseline SHA. If anything fails, stop and report; do not fix model code.

## 2. Tasks
1. **Cleanup:** merged branches that are safe to delete (delete only merged ones; report unmerged ones, e.g. old kit branches and PRs); `.gitignore` covers `.venv`, `__pycache__`, `.pytest_cache`; dead files only with proof.
2. **`docs/STATE.md`**, one self-contained document with a table of contents, plain short sentences, fish commands, each section ending `Evidence: VERIFIED / OWNER-CONFIRM / UNVERIFIED` with the command or file checked:
   - purpose and how it connects to the PEIRA site
   - layout of the repo, every file's purpose
   - inputs (`research.md`, `figures.csv`, `timeline.csv`): what each is, row counts, how many rows are `candidate` vs `verified`, which rows were agent-researched
   - the export format (schemaVersion 1, including `scenarios`, `median`, `omitted`), reproduced from `docs/data-format.md` and checked against the actual files
   - the scenario model in plain words: what it samples, which `figures.csv` rows map to which quantity, the daily loss shares, the scenarios and parameters, the output metrics, what it does NOT do
   - reproducibility: seeds, draws, how determinism is tested, fresh-clone commands
   - CI: what the workflow does
   - **Known issues:** audit the scenario export for plausibility **without changing it** — compare the cavalry and total-strength ranges in `exports/leipzig-scenarios.v1.json` against the corresponding rows in `figures.csv`, check whether S1 differs meaningfully from S0, and report numbers and your reading. Say clearly if the results look implausible or if the model's counting might double-count; do not fix it.
   - how to add a figure, rerun the exports, verify rows, and copy exports into the site (`pnpm sync:data` in the site repo)
   - how to start research repo number 2 from this one
3. Update `README.md` to be accurate and link `docs/STATE.md`.
4. Verify fresh-clone reproduction in a temp dir and quote the output.

## 3. Rules
No behaviour changes, no input changes, no export changes. Never invent a source, number, coordinate or date. Never print secrets. Never tag or release. Never force-push.

## 4. Final report (always)
Table: task → status → PR → evidence. Then: **what I deleted**, **plausibility findings on the scenario results** (numbers, not adjectives), **rows still candidate**, **sections tagged OWNER-CONFIRM or UNVERIFIED**, and the exact commands for the owner to tag the freeze.
