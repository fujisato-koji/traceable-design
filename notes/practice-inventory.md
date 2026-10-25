# Practice inventory

This note lists what was actually done on the [bread-oven](https://github.com/fujisato-koji/bread-oven) project, as raw material for the standard.
Conventions (C-nn) are what the record follows.
Incidents (I-nn) are events that showed why a convention is needed, or that one was missing.
Gaps are places where the practice falls short of the requirements in [spec/01-requirements.md](../spec/01-requirements.md).

The bread-oven record is written in Japanese.
Paths below are relative to that repository, and the terms are translated.
Inventory taken on 2026-10-25 from the main branch at that date.

## Conventions

| ID | Convention | Where | Serves |
|----|------------|-------|--------|
| C-01 | Requirements are numbered R-nn, with a lowercase letter for children (R-02a). Columns: number, requirement, origin (owner, derived, or both), design point, basis, status. Derived requirements wait for the owner to confirm them. One requirement is marked "if possible" and yields to the others. | `docs/01-requirements.md` 1.2 | S-03, S-04 |
| C-02 | The design point and the expected value share a cell: "within 20 °C; expected within 10 °C". | `docs/01-requirements.md` 1.2 | S-03 |
| C-03 | Requirement status is one of confirmed, provisional, awaiting confirmation. Provisional means the value has a source but no primary source pins it down. | `docs/01-requirements.md` 1.2 | S-01 |
| C-04 | A section "reading the basis" gives one bullet per requirement, one sentence per line, in a fixed layout a script parses. | `docs/01-requirements.md`, `tools/gen_nav.py` | S-01, S-07 |
| C-05 | Conflicts between requirements are a table: conflict, what, where it settles. | `docs/01-requirements.md` 1.3 | S-04 |
| C-06 | Each dimension is an object with value, unit, label, status, and basis, under a dotted key (`dome.thickness`). Status is decided or provisional. A decided value cites "owner decision" and a date. | `docs/data/oven.json` | S-01 |
| C-07 | Prose marks the kind of each number in brackets: calculation, estimate, unverified, provisional, owner decision with date. | all documents | S-01 |
| C-08 | Sources carry a mark by class: P primary (books, standards, laws, papers, maker data), S secondary (articles, blogs), M sales page (prices), F forum (rule of thumb, never a design point by itself). The table has mark, bibliography, URL. The retrieval date is in the header, and rows note how far the source was read (abstract only, search excerpt, archived copy, not read). Marks are not reused. | `docs/sources.md` | S-01, S-02 |
| C-09 | Decisions are dated inline ("owner decision 2026-10-21"), and a premises table lists what the owner decided. Changes keep their history ("R-13 withdrawn"). | `docs/01-requirements.md` 1.1 | S-04, S-09 |
| C-10 | Open questions are a table: number, question, waits for (owner, fire service, maker), affects. A settled row is rewritten as "(decided: what, owner decision, date)" and kept. | `docs/01-requirements.md` 1.4, `docs/02-configuration.md` 2.8 | S-09 |
| C-11 | When a requirement can be read two ways, the readings get names (reading a, reading b), and the chosen one is recorded. | `docs/01-requirements.md`, `docs/03-structural-design.md` | S-04 |
| C-12 | A "reflect to" table lists which document takes which change. | `docs/02-configuration.md` 2.9 | S-09 |
| C-13 | Independent checks are named in prose: an independent model, a different formulation, a hand calculation. Items to check at the first firing are written as pass or fail. | `docs/03-structural-design.md` | S-06 |
| C-14 | A script checks the record and writes nothing on failure (exit code 1), with a check-only mode. Codes: E1 duplicate id; E2 to E9 parts, dimensions, flows, views, steps, arrows, and requirement allocations that do not resolve; E10 unknown source mark; E11 to E13 build steps (days, kinds, missing predecessors, cycles); E14 unknown parts or requirements in build steps; E15 items (quantities, prices, status words, delivery before use); E16 parts list table differs from its data; E17 unknown keys in YAML. | `tools/gen_nav.py`, `NAVIGATOR.md` | S-07 |
| C-15 | A thermal model writes its results to data, and a script compares them with the values in the documents, stopping at a difference over 1 K or 1 minute. The model was ported and compared with the original to under 0.01 K. | `tools/gen_thermal.py`, `tools/thermal_model.py` | S-06, S-07 |
| C-16 | Tables made from data are written between markers by a script and never edited by hand. One generated file is built in CI and not committed; another is committed and checked. | `tools/gen_bom.py`, `docs/05-parts-list.md` | S-07 |
| C-17 | CI runs the model check, then the record check, then a strict site build, then publishes. | `.github/workflows/pages.yml` | S-07 |
| C-18 | Documents go in order: 1 requirements, 2 form (configuration), 3 design calculations, 4 availability, 5 parts list and cost, then appendices for operation and building. Requirements are numbered before forms are compared. When a part cannot be had, the reason and the stage to return to are written in the availability document first. When cost runs over, the owner is told at once, with the items that drive it. | `docs/index.md` | S-04, S-10 |
| C-19 | The form chapter runs: candidates, yardsticks, rough cost, comparison, selection, open questions, reflect to. Rejected options stay, briefly, at the end of the section. | `docs/02-configuration.md` | S-09, S-10 |
| C-20 | The calculation chapter opens with a table of items: item, requirement it serves, content, status. It doubles as a progress list. | `docs/03-structural-design.md` 3.1 | S-09 |
| C-21 | Each kind of data has one home: dimensions, model (parts, flows, steps, requirement allocation), build steps, items, requirements, sources. One part id threads the 3D model, the drawings, the system diagram, the steps, and the requirements. | `README.md`, `NAVIGATOR.md` | S-07 |
| C-22 | Ids carry prefixes by kind (items, build steps, batches). | `docs/data/*.yaml` | S-07 |
| C-23 | No place name or address appears. Values such as frost depth and snow load appear without the place. Weather station names are left out. | `README.md`, `docs/index.md`, `docs/sources.md` | S-14 |
| C-24 | One sentence per line. A space between number and unit. Thousands separators. °C for temperatures and K for differences. SI units. ISO dates. | all documents | S-01 |
| C-25 | The top page has a status column, updated with a dated summary on each change. | `docs/index.md` | S-09 |
| C-26 | One navigator page shows the record in seven modes (requirements, flow, system diagram, drawings, 3D, timeline, procurement). Modes register through a small contract, the URL carries the mode and the selection, and the frame draws the detail card. | `docs/navigator/`, `NAVIGATOR.md` | S-07, S-12 |

## Incidents

| ID | Date | What happened | Shows the need for |
|----|------|---------------|--------------------|
| I-01 | 2026-10-20 | An earlier answer said a chimney would roughly double the draw. An independent model showed that with a single opening the chimney's pull does not reach the chamber (exchange flow within 2 %). The claim was withdrawn before the owner relied on it. | S-06 |
| I-02 | 2026-10-18 | The build schedule and the 3D model assumed a 150 mm concrete base, while the cost counted crushed stone only. Nothing linked them at the time. | S-07 |
| I-03 | 2026-10-19 to 2026-10-20 | A new first proposal was worked out outside the repository, because the working notes named the place. Bringing it back took six pull requests. | S-09, S-14 |
| I-04 | 2026-10-20 | Work stopped near a usage limit. A pull request was merged while some of the 19 findings of its review were still open, and the next pull request carried them. | S-09 |
| I-05 | 2026-10-21 | Each pull request took two to three hours of writing, screen checks, and refutation. The owner asked for speed. Tiers of checking were set, but only in the assistant's private notes. | S-11 |
| I-06 | 2026-10-17 to 2026-10-18 | The first proposal assumed clay and sand from the site. The owner said none was available and all material had to be bought. Prices then showed every option over the budget, and the form was chosen again. | S-10 |
| I-07 | 2026-09 (other work) | When a schedule slipped, an assistant moved a deadline along with a visible milestone. The deadline was anchored to the day the equipment was first used, and the owner reverted the change. | S-04 |
| I-08 | 2026-09 (other work) | A review explained thirteen issues and the direction of each fix, without the current and proposed text. The owner could not tell what was at issue. | S-05 |
| I-09 | 2026-09 (other work) | A guideline gave formulas and thresholds with no stated source, so neither their validity nor their fit could be checked. A standard that traced its threshold to injury data and primary experiments was chosen instead. | S-02 |
| I-10 | 2026-10-17 to 2026-10-22 | The owner decided everything by answering questions in conversation, for example lowering the loaves per day from 12 to 6 and withdrawing the requirement to move the oven. The assistant wrote all the data files and recorded each decision with its date. | S-04, S-12 |

## Gaps

| Gap | Requirement |
|-----|-------------|
| The source table has no license column. | S-01 |
| Status words differ by file: decided or provisional (dimensions), confirmed, provisional, or awaiting (requirements), a tentative flag (items). | S-01 |
| Independent checks are recorded in prose, so a machine cannot tell which claims lack one. | S-06, S-07 |
| There is no hazard list. Hot surfaces are covered by one requirement. | S-08 |
| Decisions are spread inline over many documents, with no single list. | S-04, S-09 |
| Tiers of change exist only in the assistant's private notes. | S-11 |
| The rule against place names is kept by habit, with no check. | S-14 |
| The record does not say which assistant or model made each change, beyond commit trailers. | Q-03 |
