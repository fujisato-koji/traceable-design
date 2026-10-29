# Decisions

The decisions made about this standard, kept the way the standard asks a project to keep its own.
Each decision with a date was made by the owner.
A decision marked proposed has not been made, and nothing it touches is in force.

| ID | Date | What was decided | Touches |
|----|------|------------------|---------|
| D-001 | 2026-10-25 | Develop the standard in its own public repository, named traceable-design. | README |
| D-002 | 2026-10-25 | Write the standard in English. | Q-05 |
| D-003 | 2026-10-25 | License code under MIT and text under CC BY 4.0. | LICENSE |
| D-004 | 2026-10-25 | The aim is that other makers use it. | S-12 |
| D-005 | 2026-10-25 | Cover the whole life of the thing: design, building, operation, change, and removal. | 1.1, S-16 to S-18 |
| D-006 | 2026-10-25 | Publish the token measurement of the worked example, as shares and counts only. | notes/token-case-study.md |
| D-007 | 2026-10-25 | Accept the form of chapter 2 (F-1 to F-7), with a status sheet budget of 10,000 tokens as the design point and 5,000 as the expected value. Merged as #3. | chapter 2, Q-07 |
| D-008 | 2026-10-25 | Aim for closed loops across people, projects, and the standard, as the way AI is put to real use in the physical world. Merged as #4. | S-19 to S-23, README |
| D-009 | 2026-10-25 | The first cluster is individual makers and makers near the owner. | README |
| D-010 | 2026-10-25 | Keep the repositories in the traceable-design organization. | README |
| D-011 | 2026-10-25 | Data files are YAML restricted to a subset that a standard-library reader accepts. | Q-08, 3.2 |
| D-012 | 2026-10-25 | Do not redo the worked example to measure tokens; measure them on a new project instead. | S-15, pass 5 |
| D-013 | 2026-10-25 | Publish `template/` as the template repository traceable-design/template. | README |
| D-014 (proposed) | 2026-10-29 | Not yet decided. Add a model kind with design runs (MD-nn, MD-nn.nn), the rules and checks behind it, and smaller schema changes. See below. | F-2, F-5, 2.5, 3.1, 3.3, 3.9, 3.12, SKILL.md, template/ |

## D-014 (proposed): models and design runs

Status: proposed.
The owner of the standard accepts it, amends it, or declines it.
Until then the text it adds is marked "(proposed)" in [chapter 2](02-form.md) (2.11) and [chapter 3](03-rules.md) (3.12), and the current text stays in force.

### Basis

The audit of the drone trial found that the standard has no kind for a program whose output becomes a value.
A value computed by code cited a commit prose or nothing, a check covered a version of the code that no longer existed, and constants were copied from the record into code and drifted.
Three designs were compared: one new kind with nested runs (MD-nn, MD-nn.nn), runs as separate numbered records (MR-nnn), and versioned models with stamped runs (MD-nn@v, DR-nnn).
The first fits the tool and the existing rules best.
It is chosen with these grafts from the others: a param and result interface with domain, one run file per model, superseded runs kept as history, a scope line, role onboard bound to the baseline, quoted `sha-` hashes, `check.version` and `check.supersedes`, and a model card for sharing.
Version, freshness, and coverage are computed by the tool and never stored by hand.
The comparison and the audit findings are in the working notes of the drone trial and are not published here.

### Side by side

| Where | Current | Proposed |
|-------|---------|----------|
| F-2, kinds table (2.3) | No kind for a program or its runs. A Run (RN-nnn) is a run of the physical thing. | Adds Model (MD-nn) and Design run (MD-nn.nn). A design run is never a Run. See 2.11. |
| F-5, T1 row (2.6) | "A value changes on a basis already in the record (the same checked model, a newer price from the same shop)". "The same checked model" is not defined. | "The same checked model": the same id, method line, params, results, and scope, and every cited run reruns within its tolerance. |
| F-5, T0 to T3 rows (2.6) | T0 wording and layout. T1 a value on a known basis. T2 a new calculation, model, or source. T3 a requirement, a limit, a hazard control, or the configuration of something built or running. | Adds: T0 backfill of a model or run that reproduces recorded values, a restamp that moves nothing, and a requirement confirmed by an owner decision. T1 a code or input edit that keeps the model the same. T2 a new model, a changed method, params, results or scope, a cited output moving beyond its tolerance, a run outside its domain, a repair of a defect, a new awaiting requirement. T3 a change to an onboard model in an as built baseline, a change of a design point, a limit, or a hazard control, a change to a confirmed requirement. |
| 2.5 gate, design to build | "Every requirement has a design value and a verification method. Every hazard has a control. Open items that block building are closed. The parts list is priced." | "design value" reads "design point". Adds: every part has a sourced or decided price. The hazard list is not empty unless an owner decision says none apply. Every calculated value a design point rests on cites a fresh run of a model with a passing check at its current version. |
| 2.5 order of work | Five steps; hazards, parts, and models have no named place. | List hazards in 1.1 and revisit per candidate in 1.2. Record parts and interfaces in 1.2 and 1.3. Record a model before its first value. |
| N-20 (3.5) | "A T2 change cites a check whose method is refute, independent_model, or hand_calc, made by someone other than the author." | The check has result pass, and when it targets a model it carries the model's current version, one such check for each model changed. |
| N-07 (3.2) | "SI units; K for temperature differences." | SI and the units accepted for use with SI, currency codes, count, and B. Others are converted or named as an exception. |
| N-19, N-21, trailers (3.5) | `Decision:` names one decision. | `Decision:` accepts a comma list. The root commit of a template repository is exempt from N-19. |
| 3.3 smaller changes | Requirement, Part, Open item, Value, Source, Check, and Decision as listed in 3.3. | Adds requirement `values`, part `price`, open item `after`, value status `withdrawn`, source read level `query`, check `version` and `supersedes`, a list for decision `supersedes`, and section ids `{#id}` (N-48). |
| 3.9 codes | E05, E11, E20, E22 as listed. E23 and later are unused. | E05, E11, E20, E22 extended. New: E23 stale run, E24 hidden input, E25 out of domain input, E26 output and value mismatch, E27 stale table. |
| 3.9 "does not check yet" | Three items. | Adds what the gate, E11, E03, and design point text do not check. This part is already written in 3.9 because it describes the tool as it is. |

### Open questions

The questions are in 3.10 of chapter 3 and are repeated here.

| No. | Question | Waits for | Affects |
|-----|----------|-----------|---------|
| Q-15 | Whether a T1 edit that keeps a model "the same" may leave it checked at an older version between gates, or whether every code edit needs a re-check. Recommended: allow it between gates. | owner | F-5, N-44 |
| Q-16 | Whether a slow run may be marked `rerun: manual` and proved only at the next version change and at gates, and how long unused superseded runs are kept. | owner | N-43 |
| Q-17 | Depends on Q-11. Where a project keeps the home's index and the vendored files of a shared model, and how often the fetch runs. | owner | N-51 |

### What the reference tool does with it

The tool implements a safe subset, with every new field optional and the schema still 1, so that the worked example and the template pass as before.
The list of what is implemented and what is not is at the end of 3.12.
The tool can be merged on its own without accepting the rest, but then the checks that rest on rules not in force have no rule to cite, so the owner should decide D-014 before relying on them.
