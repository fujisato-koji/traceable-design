# 3. Rules and checks

This chapter is the third pass.
It turns the form of [chapter 2](02-form.md) into rules a project follows and checks a script runs.
Each rule (N-nn) names the requirements of [chapter 1](01-requirements.md) it serves and who or what checks it.
Each check code (E-nn) is something a script refuses.

The tools named here (`tdr check`, `tdr get`, and so on) are the reference implementation in [tools/tdr.py](../tools/tdr.py), which uses the Python standard library only.
The standard requires their behaviour, not their names (Q-09).

## 3.1 Layout of a record

```text
record/
  requirements.yaml   R-nn
  values.yaml         dotted keys
  sources.yaml        P12, S3, M5, F2
  decisions.yaml      D-nnn
  open.yaml           Q-nnn (questions, findings, notices)
  hazards.yaml        H-nn
  parts.yaml          part ids
  interfaces.yaml     I-nn
  checks.yaml         K-nnn
  shared.yaml         shared items cited, and responses to notices
  config/B-nn.yaml    baselines: as designed, as built, as operated
  runs/RN-nnn.yaml    one file per run
  procedures/OP-nn.yaml
docs/                 reasoning, one file per stage, sections with ids
STATUS.md             generated, never edited by hand
```

| Rule | Text | Serves | Checked by |
|------|------|--------|------------|
| N-01 | Each kind of fact lives in one place in `record/`. Prose in `docs/` cites facts by id and never restates a value except in a generated table. | S-07, S-15 | E10 |
| N-02 | Tables in `docs/` that show facts are generated between markers and never edited by hand. | S-07 | E10 |
| N-03 | `STATUS.md` is generated on every change. | S-09, S-15 | E10, E14 |

Source marks keep the form of the worked example (P12, not P-12), so that they do not look like the requirement ids of this standard.

## 3.2 Data format (settles Q-08)

### Candidates

| Yardstick | YAML, strict subset | JSON | TOML |
|-----------|---------------------|------|------|
| People can review a diff | good | fair: quotes and braces everywhere | good |
| Tokens to read the same facts | fewer: no quotes or braces for most values | more | fewer |
| Lists of records with nested lists | good | good | poor: arrays of tables are awkward |
| Read with the standard library only (S-13) | needs a small reader for the subset | yes | yes in Python 3.11 and later |
| Silent misreading | none inside the subset; flow style can cut a value at a comma or ` #` (the accident behind E17 of the worked example) | none | rare |

### Selection

YAML 1.2, restricted to a subset that a small reader in the reference tools accepts.
The reader uses only the standard library, and anything outside the subset fails to parse (E01), so the subset is enforced by construction.

| Rule | Text | Serves | Checked by |
|------|------|--------|------------|
| N-04 | Block style only. No flow style (`{}` or `[]` on one line), no anchors or aliases, no tags, one document per file. | S-07, S-13 | E01 |
| N-05 | Comments stand on their own lines; nothing after a value is a comment. A string that contains ` #` or `: `, or starts with a character YAML treats specially, is quoted, so that no value is ever cut short silently. | S-07 | E01 |
| N-06 | Each file has three top-level keys: `kind:`, `schema:` (the version of its schema), and `items:` (the list of facts). Keys and allowed values are lowercase with underscores. An empty list is the key with no value. Unknown keys are refused. | S-07 | E01, E21, E22 |
| N-07 | UTF-8, LF line ends. Dates as YYYY-MM-DD. A number and its unit are separate fields. SI units; K for temperature differences. | S-01 | E01, E22 |

## 3.3 Kinds of fact

Required fields are in bold.
Every list of references (`basis`, `touches`, `affects`, `controls`) holds ids of this record or global ids of shared items (3.6).

| Kind | Fields | Allowed values |
|------|--------|----------------|
| Requirement | **id**, **text**, **origin**, **design_point**, expected, **verify**, **basis**, **status**, parent, parts | origin: owner, derived. verify: inspection, analysis, demonstration, test. status: awaiting (derived, not yet confirmed by the owner), confirmed, withdrawn. |
| Value | **key**, **v**, unit, **status**, **basis** | status: decided, sourced, calculated, measured, assumed. |
| Source | **id**, **class**, **title**, url, **retrieved**, **license**, **read**, note | class: P primary, S secondary, M sales page, F forum, matching the letter of the id. license: a name, or unknown. read: full, partial, abstract, excerpt, archived, not_read. `retrieved` may be left out only when read is not_read. |
| Decision | **id**, **date**, **by**, **what**, options, **touches**, supersedes | by: owner, operator (within a delegation, Q-06). |
| Open item | **id**, **kind**, **text**, **waits_for**, **affects**, **opened**, raised_by, phase, run, blocks, closed_by, closed | kind: question, finding, notice. phase: design, build, operate, change, remove. blocks: the gate it must be closed before. closed_by: a decision or a check. |
| Hazard | **id**, **text**, **phases**, **at_risk**, **controls** | controls: requirement ids and procedure step ids. |
| Part | **id**, **name**, parent | |
| Interface | **id**, **between** (two part ids), **carries**, values | carries: load, heat, gas, liquid, power, signal, smoke, other. |
| Check | **id**, **target**, **tier**, **method**, **result**, **by**, **date**, detail | method: script, refute, independent_model, hand_calc, inspection, analysis, demonstration, test, measurement. result: pass, fail, partial. |
| Baseline | **id**, **kind**, **date**, **decision**, deviations | kind: as_designed, as_built, as_operated. Each deviation: key, design value, built value, decision. |
| Run | **id**, **date**, **procedure**, conditions, measured, deviations, findings | measured: key, value, unit, how measured. |
| Procedure | **id**, **title**, **steps** | Each step: id (OP-nn.nn), action, values by key, controls (hazard ids), limits (keys). |
| Shared citation | **ref**, **used_for**, responses | ref: a global id with a version. Each response: notice, answer (adopted, not_applicable, open), by_id (a decision or an open item). |

| Rule | Text | Serves | Checked by |
|------|------|--------|------------|
| N-08 | A value's status matches its basis: decided cites a decision, sourced a source, calculated a check or a section of reasoning, measured a run, and assumed an open item. | S-01, S-17 | E04, E05 |
| N-09 | A design point never rests on forum sources alone. A borrowed threshold notes the conditions it was derived under in its source's note. | S-02 | E06 |
| N-10 | Every requirement with a numeric measure has a design point; an expected value never appears without one. | S-03 | E07 |
| N-11 | Every requirement carries a verification method. | S-03, S-17 | E08 |
| N-12 | A finding names the item it concerns, the phase, and who raised it, and a finding from a run names the run. | S-19 | E18 |
| N-13 | A deviation in building cites a decision. | S-16 | E19 |
| N-14 | Every hazard has at least one control. Every value in a procedure step resolves to a value key, and every hazard control appears in at least one procedure step before the build to operate gate. | S-08, S-18 | E09, E17 |

## 3.4 How the assistant reads

| Command | Returns |
|---------|---------|
| `tdr status` | Writes `STATUS.md`: phase and next gate, baseline in force, open items grouped by whom they wait for, the last ten decisions, unanswered notices, failing checks, and next steps. |
| `tdr get <id or key>` | The item, its status, and its basis, one level deep, in a few lines. |
| `tdr refs <id or key>` | Every item that refers to it. |
| `tdr brief <ids>` | What a helper needs for a task on those ids: the items, their requirements and values, the interfaces of the parts, open items that touch them, and the ids of reasoning sections to read. |

| Rule | Text | Serves | Checked by |
|------|------|--------|------------|
| N-15 | `STATUS.md` stays within 10,000 tokens (design point); 5,000 is the expected value. Tokens are estimated as ASCII characters divided by 4 plus other characters divided by 1.5. | S-15 | E14 |
| N-16 | A helper starts from a brief, plus the question. It reads documents only by section id, when the brief points to them. | S-15 | owner review |
| N-17 | The lead conversation ends at every gate, and when its context passes 200,000 tokens. The next one starts from `STATUS.md`. | S-09, S-15 | owner review |
| N-18 | Values are looked up with `tdr get`, not by searching documents. | S-15 | owner review |

The rules checked by owner review are carried by the Agent Skill (3.8), since no script can see how the assistant read.
`tools/usage_report.py` measures whether they held.

## 3.5 Tiers and gates

A change states its tier in its description with trailer lines.

```text
Tier: T2
Checks: K-014
Decision: D-022
```

| Rule | Text | Serves | Checked by |
|------|------|--------|------------|
| N-19 | Every change states its tier (T0 record, T1 value, T2 claim, T3 limit). | S-11 | E11 |
| N-20 | A T2 change cites a check whose method is refute, independent_model, or hand_calc, made by someone other than the author. | S-06 | E11 |
| N-21 | A T3 change cites a decision, and the hazards whose controls it touches are listed in that decision. A T3 change to something running is not merged during a run. | S-04, S-08 | E12 |
| N-22 | `tdr check --gate <gate>` adds the conditions of that gate in 2.5 of chapter 2. A gate is passed by a decision that cites a clean gate check. | S-04, S-09 | E09, E16, E20 |

## 3.6 Shared items

A shared item lives in a public repository and has a global id: `owner/repo#id@version`.
A project cites it in `shared.yaml` and uses it in a basis like any local id.

| Rule | Text | Serves | Checked by |
|------|------|--------|------------|
| N-23 | A published version never changes. A wrong one is marked withdrawn, with a reason, and kept. | S-20 | E15 |
| N-24 | Each version lists the checks that verified it and who made them. | S-06, S-20 | E15 |
| N-25 | A change or a withdrawal of an item creates a notice in every project that cites it, as an open item of kind notice. | S-22 | E16 |
| N-26 | Each notice gets an answer before the next gate: adopted (with the tier of the change it brings), not_applicable (tier T0), or open with whom it waits for. | S-22 | E16 |
| N-27 | A project that checks, corrects, or refreshes a shared item offers the result back to the item's home, after its own private-name check passes. | S-23, S-14 | owner review |
| N-28 | A shared item carries derived values only, and passes the private-name check of the project that publishes it. | S-14 | E13 |

## 3.7 Private facts

| Rule | Text | Serves | Checked by |
|------|------|--------|------------|
| N-29 | Private facts live in a private store outside the public record, with the same ids. A value derived from one has the basis `private:<id>`. | S-09, S-14 | E03 |
| N-30 | The list of private names lives in the private store. `tdr check` reads it from a path or an environment variable, fails on any match in the public record, and never prints the name it found. | S-14 | E13 |

## 3.8 Rules for the assistant

These rules cannot be checked by script.
They go into the Agent Skill, and the owner checks them in review.

| Rule | Text | Serves |
|------|------|--------|
| N-31 | Before comparing forms, ask the questions that can rule a form out (2.5 of chapter 2), and record each answer as a decision or an open item. | S-10 |
| N-32 | Write a value into the record with its status and basis at the moment it is first used, never later. | S-01 |
| N-33 | Never relax a requirement, a limit, a deadline, or a margin. Propose the change, with the current and the proposed version side by side and a recommendation. | S-04, S-05 |
| N-34 | Say how far each source was read, and never report a source as read when only a summary was seen. | S-02 |
| N-35 | For a T2 claim, start a checker with the claim and its inputs by id, told to refute it, and record the result as a check. | S-06 |
| N-36 | Tell the owner at once when a limit is likely to be passed, naming the items that drive it. | S-04 |
| N-37 | During a run, advise only. When a limit is reached, stop the step and hand the decision to the operator or the owner. | S-04 |

## 3.9 Check codes

| Code | Refuses | Rules |
|------|---------|-------|
| E01 | A file outside the YAML subset, or without `kind` and `schema` | N-04 to N-07 |
| E02 | A duplicate id | all |
| E03 | A reference to an id, key, or private id that does not exist | all |
| E04 | A value without a status or a basis | N-08 |
| E05 | A status that does not match its basis | N-08 |
| E06 | A design point resting on forum sources alone | N-09 |
| E07 | A numeric requirement without a design point, or an expected value without one | N-10 |
| E08 | A requirement without a verification method | N-11 |
| E09 | A hazard without a control, or (at the build to operate gate) a control in no procedure step | N-14, N-22 |
| E10 | A generated table or `STATUS.md` that differs from what the data give, or a value restated in prose | N-01 to N-03 |
| E11 | A change without a tier, or a T2 change without an independent check | N-19, N-20 |
| E12 | A T3 change without a decision | N-21 |
| E13 | A private name in the public record or in a shared item | N-28, N-30 |
| E14 | `STATUS.md` over its token budget | N-15 |
| E15 | A shared item cited without a version, a changed published version, or a version without its checks | N-23, N-24 |
| E16 | A notice without an answer at a gate | N-25, N-26 |
| E17 | A procedure value that does not resolve | N-14 |
| E18 | A finding without its item, phase, or who raised it | N-12 |
| E19 | A deviation without a decision | N-13 |
| E20 | A gate condition of 2.5 of chapter 2 not met | N-22 |
| E21 | An unknown key | N-06 |
| E22 | A required field missing, a value not among the allowed values, an id, key, or date in the wrong form, or a source class that does not match its id | N-06, N-07 |

### What the reference tool does not check yet

- E15 checks only that a citation has a version in the right form. Whether a published version changed, and whether a version lists its checks, need the item's home and are left to a later service.
- E10 compares `STATUS.md` and generated tables. It does not find a value restated in prose.
- N-20's "someone other than the author" is not compared with the change's author.
- E11 ignores the result and the target of the check it is given. The `design_build` gate does not check that a parts list exists or is priced, or that any hazard is listed. Values written inside the text of a design point are not references. Nothing compares the constants a model uses with the record (E24 below is proposed).
- E03 resolves the `#section` of a docs reference only against `{#id}` headings (N-48, proposed), and only in a file that has at least one such heading.

## 3.10 Open items

| No. | Question | Waits for | Affects |
|-----|----------|-----------|---------|
| Q-09 | Whether the commands of 3.4 are part of the standard or only a reference implementation. This chapter assumes the behaviour is required and the names are not. | owner | 3.4 |
| Q-10 | How the worked example moves its requirements, sources, decisions, and open items into `record/`. | pass 6 | 3.1 |
| Q-13 | Whether the token estimate of N-15 is close enough, checked against a real tokenizer on the trial. | measurement on the trial | N-15 |
| Q-15 (proposed, D-014) | Whether a T1 edit that keeps a model "the same" may leave the model checked at an older version between gates (reruns within tolerance, a re-check at the gate), or whether every code edit needs a re-check. Recommended: allow it between gates. | owner | F-5, N-44 |
| Q-16 (proposed, D-014) | Whether a slow run (for example a differential evolution search) may be marked `rerun: manual`, proved only at the next version change and at gates, and how long unused superseded runs are kept. | owner | N-43 |
| Q-17 (proposed, D-014) | Depends on Q-11. Where a project that cites a shared model keeps the home's index and the vendored files, and how often the fetch runs. | owner | N-51 |
| Q-14 | How a project learns that the tool, the skill, or the template has a new version, and how it updates its copies: S-22 applied to the standard's own tools. Until then, copies are updated by hand. | owner | S-22, N-25, N-26 |

## 3.11 Reflect to

| Where | What |
|-------|------|
| Chapter 2, 2.3 | Source marks take the form P12 (3.1). |
| Pass 4 | Done in [tools/tdr.py](../tools/tdr.py) (the YAML subset reader, `check`, `status`, `get`, `refs`, `brief`, `tier`, and an MCP server with the same calls), [skill/traceable-design/SKILL.md](../skill/traceable-design/SKILL.md) (3.8 and the order of work), and [template/](../template/) (the layout of 3.1). |

## 3.12 Proposed: models and design runs (D-014)

Everything in this section is proposed by [D-014](decisions.md).
It is not in force until the owner accepts D-014.
Every rule carries "(proposed)" in its first cell.
The evidence is the audit of the drone trial (pass 5): its record held computed values with no way to say which program version made them.
[Chapter 2, 2.11](02-form.md) holds the matching amendments to F-2, F-5, and the design to build gate.

### Layout (proposed)

```text
record/
  models.yaml           MD-nn
  model_runs/MD-nn.yaml design runs MD-nn.nn, one file per model
```

### Kinds added (proposed)

| Kind | Fields | Allowed values |
|------|--------|----------------|
| Model | **id**, **title**, **role**, **files**, **entry**, **method**, **basis**, **scope**, **params**, **results**, uses, part, from, withdrawn | role: analysis, onboard. files: paths inside the project, in hashing order. params: name, unit, optional min and max. results: name, unit. uses: ids of other models. part: a part id, required for onboard. method: one line, no numbers. |
| Design run | **id** (MD-nn.nn), **model**, **date**, **by**, **version**, **stamp**, **command**, inputs, settings, seed, outputs, tol, writes, note | version, stamp: sha-<12 hex>. inputs: param, and one of key (a value key) or run (a run id). settings: name, v, unit. outputs: result, key (never the number). writes: files the run writes. |

### Smaller changes to existing kinds (proposed)

| Change | Text |
|--------|------|
| Requirement `values` | Optional list of the value keys its design point is judged on. E03 resolves them. |
| Part `price` | Optional value key of the part's price. E03 resolves it. |
| Open item `after` | Optional list of open items it waits on. E03 resolves them. |
| Value status `withdrawn` | A value that is dead but still targeted by a check or a superseded run. Kept with its reason. |
| Source read level `query` | A dataset service where only some points were queried. |
| Check `version`, `supersedes` | `version` is the model version the check saw. `supersedes` is a check, or a list of checks, that this one replaces. |
| Decision `supersedes` | A single id or a list of ids. |
| Decision trailer | `Decision:` accepts a comma list, as `Checks:` does (N-19, N-21). The root commit of a template repository is exempt from N-19. |
| Section ids | A section id is a heading ending in `{#id}` (N-48). |

### Rules (proposed)

| Rule | Text | Serves | Checked by |
|------|------|--------|------------|
| N-38 (proposed) | A program whose output becomes a value, or which will run in the thing, is a model (MD-nn) in `record/models.yaml`. Its version is `sha-` and the first 12 hex digits of the SHA-256 of, for each listed file in order, the path, a NUL byte, the bytes with CRLF turned into LF, and a NUL byte, then, for each model it uses in order, the text `uses`, a NUL byte, that model's version, and a NUL byte. The tool computes the version and it is never stored on the model. | S-01, S-07, S-13, S-20 | E03, E22 |
| N-39 (proposed) | A value a model produced has status calculated and cites its run (MD-nn.nn), and may add the docs section of its reasoning. A run lists output keys, never numbers, so each number stays in one place. Superseded runs are kept as history, and prose cites the old run id instead of restating its numbers. | S-01, S-07 | E05, E26 |
| N-40 (proposed) | A run states its date, who, model version, stamp, exact command, inputs (value keys mapped to params, or ids of runs whose results it reads), settings (the non design numbers, such as duration and time step), seed, tolerance, and the files it writes. Nothing outside these changes the result: no unlisted file, clock, or unpinned seed. The stamp is `sha-` and 12 hex digits of the SHA-256 of the compact JSON of the version, the inputs (param, key, number, unit; for a run input, that run's stamp), the settings, the seed, and the command. A number written 18 or 18.0 reads the same. | S-01 | E03, E22, E24 |
| N-41 (proposed) | A run that a value cites, or that a check not superseded cites, is fresh: its version and stamp recompute. A change that edits a model's files, a used model, or an input reruns the runs it affects and updates their stamps in the same change. This carries F-6 "values in documents against models" into this chapter. | S-07, S-17 | E23 |
| N-42 (proposed) | A model reads keyed values from the record, through a reader built on `load_yaml`, never from literal copies. Every constant that shapes a result is a value key or a run setting. | S-07 | E24, project tests, owner review |
| N-43 (proposed) | A file a cited run writes is listed in exactly one cited run's `writes`. Its first 256 bytes carry `tdr-run: <run id> <stamp>`. It holds no date, runtime, or machine name, is committed or ignored by git, and is never a basis. The project's CI reruns each run and compares the values citing it within tolerance (slow runs: Q-16). | S-07 | E23, project CI |
| N-44 (proposed) | A check of a model or a run names the model version it saw (`version`). A defect a check returns is a finding that affects the model, closed by a re-check at the repaired version. A later passing check may supersede an earlier partial or failing check of the same target, which the status sheet then hides. | S-06, S-09 | E22, E11 |
| N-20 amended (proposed) | A T2 change cites, for each model or calculation it adds or changes, a check with result pass and method refute, independent_model, or hand_calc, made by someone other than the author and, when it targets a model, at that model's current version. | S-06 | E11 |
| N-45 (proposed) | Each part has a price: a field `price` naming a value key (sourced, or assumed with an open item at design time). At the design to build gate every part's price is sourced or decided. | S-03 | E03, E20 |
| N-46 (proposed) | Hazards to people and property are listed from step 1.1 and revisited for each candidate form. An empty hazard list passes a gate only with an owner decision saying none apply. | S-08, S-10 | E20 |
| N-47 (proposed) | A number in a design point is cited by value key, and a requirement lists in `values` the keys its design point is judged on. E03 resolves them, E06 follows them, and `tdr brief` and the gate use them. | S-01, S-02, S-03 | E03, E06, E20 |
| N-48 (proposed) | A section id is a heading that ends in `{#id}` (lowercase letters, digits, hyphens). E03 resolves the `#fragment` of a docs reference against the ids of that file. A file with no `{#id}` heading is not checked, so records written before this rule stay valid. GitHub does not render `{#id}`; the standard accepts that. | S-07 | E03 |
| N-49 (proposed) | A value may have status withdrawn, with its reason in the docs, and is kept while a check or a superseded run still targets it. Nothing current cites a withdrawn value as a basis, in a requirement's `values`, or as the input of a cited run. | S-07 | E05 |
| N-50 (proposed) | A model of role onboard names its part. Its version is listed in the as built baseline, and any change after that is T3. | S-16, S-04 | E12, E22 |
| N-51 (proposed) | A shared model is published as a card `shared/MD-nn@sha-....yaml`, generated and immutable except for withdrawal and appended checks. The card carries the files with hashes, entry, params and results with domain, scope, the constants with value, status, and the basis resolved to source title and read level, and its checks. Params carry no private defaults, and the card passes the private name check. A project cites it as `owner/repo#MD-nn@sha-...`, vendors the files, and E15 verifies the hash offline. The home's index is fetched outside the tool, and a newer or withdrawn version becomes a notice. | S-20, S-22, S-23 | E13, E15, E16 |
| N-52 (proposed) | A project records each gap it finds in the standard as an open item (2.11, F-8). | S-21 | owner review |
| N-07 amended (proposed) | Allowed units are SI and the units accepted for use with SI (h, d, deg, L), currency codes (JPY), count, and B. Other units are converted (for example Wh/kg to J/kg) or named as an exception in the decision. | S-01 | E22 |

### Check codes (proposed)

| Code | Refuses | Rules |
|------|---------|-------|
| E05 extended (proposed) | calculated may cite a run (MD-nn.nn). measured never cites a design run. assumed cites an open item that lists the key in its `affects`. A withdrawn value is never a basis. | N-08, N-39, N-49 |
| E11 extended (proposed) | A T2 change whose cited check does not have result pass, or does not carry the current version of a model it targets. | N-20, N-44 |
| E20 extended (proposed) | At design_build: no parts, a part without a sourced or decided price, an empty hazard list without an owner decision, or a design point key that rests on a stale, unchecked, out of domain, or withdrawn run. | N-45, N-46, N-47 |
| E22 extended (proposed) | Id forms MD-nn and MD-nn.nn. version and stamp not of the form `sha-` and 12 hex digits (written in quotes). check.version missing when a target names a model. role not analysis or onboard, or onboard without a part. A cycle in `uses`. A run input that is not a param, or an output that is not a result, of its model. | N-06, N-38, N-40, N-44, N-50 |
| E23 (proposed) | A cited run is stale: its recorded version or stamp does not recompute, or a used model changed. Or a file it writes lacks its tag. The message prints the current version and stamp. | N-41, N-43 |
| E24 (proposed) | A hidden input: a value key named in the files of a model, or of a model it uses, that the run does not list among its inputs. | N-40, N-42 |
| E25 (proposed) | A run input outside the min or max of its param, unless a passing check targets that run at its stamp. | N-40 |
| E26 (proposed) | A run that some value cites lists an output key that is not a calculated value citing that run, or a value cites a run that does not list its key. Runs that no value cites are history and are not compared. | N-39 |
| E27 (proposed) | A generated docs table or `STATUS.md` is stale (moved out of E10). `tdr tables` regenerates the tables. | N-01, N-02 |

### What the reference tool implements of this section

The tool implements the new kinds `model` and `model_run` (loaded when the files exist), the smaller schema changes of the table above, `{#id}` resolution in E03 (N-48), E05 for runs and withdrawn values, E22 for the new kinds and fields, E23, E26, the comma list in the `Decision` trailer, and the commands `tdr stamp <MD id>` (prints the version and stamp to write) and `tdr tables` (regenerates the generated tables).
Every new field is optional and the schema stays 1, so records without models are unchanged.
It does not yet implement E11 extended, E20 extended, the `assumed` rule of E05 extended, E24, E25, E27 (stale tables are still reported as E10), `tdr run`, `tdr publish`, the model lines of `get`, `brief`, and `status`, the allowed unit list, the baseline `models` list of N-50, or the sharing card of N-51.
