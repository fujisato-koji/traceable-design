# 1. Requirements of the standard

This chapter is the first pass of the standard, written the way the standard asks a design to start.
It numbers what the standard must achieve before choosing any rules.
Rules, file formats, and checks come in later chapters and must each serve a requirement here.

Evidence marks (C-nn for conventions, I-nn for incidents) point to [notes/practice-inventory.md](../notes/practice-inventory.md).

## 1.1 Scope and terms

The standard covers the life of a physical thing (a structure, a device, a piece of equipment) when an AI assistant does most of the research, calculation, and writing.
The life runs through design, building, operation (use and maintenance), change, and removal.
The standard covers the record of the thing: requirements, values, sources, decisions, checks, procedures, run logs, and the documents and views made from them.
It does not make the thing safe by itself.
It makes the reasoning behind the thing visible, so that people can judge it.

| Term | Meaning |
|------|---------|
| Owner | The person who wants the thing and holds the decisions. In a personal project, the owner is often also the builder and the operator. |
| Operator | The person who runs the thing within the limits the owner set. |
| Assistant | The AI that researches, calculates, writes the record, proposes options, and advises in operation. |
| Checker | Anything that checks the assistant's output independently: a script, a second assistant session told to refute a claim, or a person. |
| Record | Everything written about the thing, kept in plain files under version control. |
| Value | A number that shapes what gets built or how it is run (a dimension, a temperature, a load, a price, a duration, a limit). |
| Basis | Where a value comes from: a source, a calculation, an owner decision, or a measurement. |
| Design point | The value a requirement is judged against (pass or fail). |
| Expected value | The value the design is hoped to reach. It never replaces the design point. |
| Configuration | The set of values that describe the thing at one stage: as designed, as built, or as operated now. |
| Run | One use of the thing (a firing, a test, a campaign). |
| Operating limit | A value that must not be passed during a run without a decision. |
| Decision | A choice the owner made, with its date. |
| Open item | A question not yet decided, or a finding not yet resolved, with who it waits for. |

## 1.2 Requirements

Origin is one of: practice (seen to work, or seen to be missing, on a real project), derived (follows from the aim of the standard), owner (the owner set it).
Status is draft for every row until the standard reaches its first release.

| ID | Requirement | Design point (pass or fail) | Expected value | Origin | Status |
|----|-------------|-----------------------------|----------------|--------|--------|
| S-01 | Every value is traceable | A check finds no value without a status and a basis, and every source mark resolves to an entry detailed enough to find the source again. | A reader picks any value and reaches the page, the script, the dated decision, or the run within five minutes. | practice | draft |
| S-02 | Each basis states its strength and fit | No forum or rule-of-thumb value stands alone as a design point, and every borrowed threshold notes the conditions it was derived under. | Values trace back to a physical phenomenon or an experiment. | practice | draft |
| S-03 | Margins are visible | Every requirement with a numeric measure has a design point, and an expected value appears only beside it. | The first use checks each design point as a pass or fail item. | practice | draft |
| S-04 | The owner holds the decisions | Every change to a requirement, a limit, a deadline, or an operating limit links to a dated owner decision. | The assistant raises a likely breach of a limit before it happens, naming the items that drive it. | practice | draft |
| S-05 | The owner can decide from the report alone | Every proposed change to a requirement, a value, or a text shows the current and the proposed version side by side, with a recommendation. | The owner decides without opening another file. | practice | draft |
| S-06 | Claims are checked before they drive a decision | Each claim a decision rests on carries a record of an independent check and its result. | The independent check is made by a separate assistant session told to refute the claim. | practice | draft |
| S-07 | Consistency is checked by machine | Every change runs checks that fail on a broken reference, or on a generated table that differs from its data. | No value is written in two places; every other place is generated from the one. | practice | draft |
| S-08 | Hazards are listed and covered | Every hazard to people or property in building, using, maintaining, and removing the thing is listed and maps to at least one requirement. | Each hazard has a check that the first build or first use can carry out. | derived | draft |
| S-09 | The work can be resumed from the record | The current configuration, the decisions, and the open items with whom they wait for are all in the record. | A fresh assistant session given only the record answers what is decided, what is open, and what comes next, correctly, in design and in operation. | practice | draft |
| S-10 | Late findings flow back to where they belong | Every change to the form or the design caused by availability, cost, building, or operation has a recorded reason and the stage it returns to. | No requirement is found missing after the form is chosen. | practice | draft |
| S-11 | Effort scales with risk | The standard defines tiers of change, and each change states its tier. | A change that only records a decision goes from request to merge in one short session. | practice | draft |
| S-12 | No systems engineering training is needed | The owner never has to edit a data file by hand. | A first-time maker finishes the small example in one session. | practice | draft |
| S-13 | Not tied to one assistant or tool | The data are plain files (Markdown, YAML, JSON), and the checks run on a standard language runtime without a network or a paid service. | A different assistant continues the same project without changing the files. | derived | draft |
| S-14 | Private facts stay out of the public record | A check against a list of private names (places, stations, addresses) passes on every change. | (none beyond the design point) | owner | draft |
| S-15 | The assistant reads little | A status sheet (current configuration, values in force, decisions, open items) fits within a set token budget, every delegated task names the ids and files it needs, and values are looked up by id rather than by reading documents. | A change costs half the tokens it cost on the worked example. | practice | draft |
| S-16 | The record follows the thing through its life | The record keeps the as-designed and the as-built configurations apart, and every deviation in building links the design value, the built value, and the owner's decision. | Anyone can tell from the record what is standing now, without visiting it. | derived | draft |
| S-17 | Operation closes the loop | Each design point gets a result (pass, fail, or not yet) from the first use, and each measured value names the run that measured it. | After each run, a script compares the measurements with the model's predictions, and each difference goes back to the stage that owns it. | practice | draft |
| S-18 | Procedures come from the record | Every value in an operating or maintenance procedure resolves to a value in the record, and every hazard control of S-08 appears in a procedure step. | Changing a value in the record changes the procedure without hand editing. | practice | draft |

## 1.3 Reading the requirements

### Traceability (S-01 to S-03)

- S-01: A number with no basis cannot be checked, corrected, or reused.
    An assistant can produce such numbers fluently, so the record has to make their absence visible.
    In practice, each value carried a status and a basis (C-06), and sources had marks that a script resolved (C-08, C-14).
- S-02: Tracing a value to a source is not enough if the source is weak or was derived for other conditions.
    In practice, sources were classed as primary, secondary, sales page, and forum, and forum values were never used as design points by themselves (C-08).
    In other engineering work, a guideline formula with no stated source could not be checked for validity or fit, and a standard that traced its threshold to injury data was chosen instead (I-09).
- S-03: An optimistic number taken as the budget hides the margin.
    In practice, each requirement carried a design point and, where useful, an expected value in the same cell (C-02).

### Authority (S-04 and S-05)

- S-04: The assistant works fast and fills gaps on its own, which includes quietly relaxing things.
    In other engineering work, an assistant moved a deadline along with a visible milestone, while the real anchor was the day the equipment was first used (I-07).
    In practice, decisions carried dates and the changes kept their history (C-09, I-10).
    In operation the same holds for operating limits.
    The assistant advises, a limit reached stops the step, and the owner or the operator decides.
- S-05: A description of an issue without the change itself left the owner unable to judge (I-08).

### Verification (S-06 to S-08)

- S-06: The assistant that made a claim is the worst placed to find its flaw.
    In practice, a claim that a chimney would roughly double the draw was refuted by an independent model before the owner relied on it (I-01).
- S-07: With many files, two of them will disagree unless a machine says so.
    In practice, the build schedule and the 3D model assumed a concrete base while the cost counted crushed stone only, and nothing linked them (I-02), and checks E1 to E17 were added one by one (C-14).
- S-08: No systematic hazard list existed in practice; hot surfaces were covered by one requirement only.
    The requirement is derived from the aim of letting other people build and run what is designed.

### Continuity (S-09 and S-10)

- S-09: Conversations end, and usage limits stop work in the middle.
    In practice, a new proposal was developed outside the repository and took six pull requests to bring back (I-03), and a pull request was merged with findings still open when a limit was reached (I-04).
    Operation spans years, so the record will be read by assistants and people who never saw the design work.
- S-10: In practice, choosing a form before the requirements were numbered was avoided on purpose (C-18).
    Availability and prices overturned the first proposal twice, and each time the reason and the stage to return to were recorded first (I-06).
    Building and operation will find things the design missed, and they flow back the same way.

### Use (S-11 to S-14)

- S-11: Full checking of every change was too slow, and the owner asked for speed (I-05).
    The tiers existed only as the assistant's private notes, not in the record.
- S-12: In practice, the owner decided by answering questions in conversation, and the assistant wrote all the data files (I-10).
- S-13: A standard tied to one vendor cannot be open in the sense this repository aims at.
    A thing in operation outlives the assistant that designed it.
- S-14: In practice, the place was never named, and values such as frost depth were given without it (C-23).

### Economy (S-15)

- S-15: An assistant pays for every token it reads, on every turn, again.
    In practice, re-reading took most of the cost, not writing (I-11).
    Delegated helpers each re-read the whole design, and the main conversation carried its full history for hundreds of turns.
    The tools of systems engineering are the remedy.
    Allocation and interface control let a helper take only the part it works on, a baseline lets a new session start from one sheet, a queryable model answers a value in one line, and a verification plan sends only the claims that need judgment to an assistant.
    Systems engineering used to be too heavy for small projects because people had to keep its structure by hand.
    With an assistant keeping the structure, the structure pays for itself in tokens.
    In operation this matters more, because questions come during a run and need short answers.

### Life (S-16 to S-18)

- S-16: A design record that stops at the drawings cannot say what was actually built.
    In practice, a change planned for operation (start without the chimney, add it later by a recorded rule) was kept as two configurations of one record (C-28).
    No as-built record exists yet, because the worked example is not built.
- S-17: Calculated values stay unverified until the thing runs.
    In practice, the items to check at the first firing were written as pass or fail (C-13), and model values were marked unverified (C-15).
- S-18: A procedure written by hand drifts from the design it came from.
    In practice, the tables of the firing procedure were checked against the thermal model by script (C-27).

## 1.4 Conflicts between requirements

| Conflict | What | Where it settles |
|----------|------|------------------|
| S-06 and S-11 | Independent checks are the most expensive step. | The tiers of S-11 decide which claims need an independent check: new claims a decision rests on, not recorded decisions or wording. |
| S-06 and S-15 | An independent checker has to read before it can refute. | The checker gets the claim and its inputs by id, not the whole record. This also keeps it independent of the author's reasoning. |
| S-09 and S-14 | Resuming from the record needs every fact, but private facts must stay out. | Private facts live in a separate private store; the public record keeps the derived values and notes that a private fact exists. |
| S-14 and S-17 | Run logs carry dates, times, and local conditions that can point to a place. | Run logs keep the measured values in the public record and leave the place, the station, and the exact local conditions in the private store. |
| S-01 and S-12 | Full traceability is a burden a first-time maker will not carry. | The assistant writes every status and basis; the owner only decides. |
| S-12 and S-16 | Recording what was built asks more of the builder. | The builder gives photos, notes, or answers; the assistant writes the as-built record. |
| S-07 and S-13 | Machine checks tend to grow dependencies. | Checks are plain scripts with no network access and no paid service. |

## 1.5 Open questions

| No. | Question | Waits for | Affects |
|-----|----------|-----------|---------|
| Q-01 | Should a design published under this standard carry a standard notice about safety and liability, and in what words? | owner | S-08 |
| Q-02 | Is the owner always one person, or should the standard cover a group of owners and how they settle a disagreement? | owner | S-04 |
| Q-03 | Should the record say which assistant and which model produced each change? | owner | S-01, S-13 |
| Q-04 | Should the standard use the terms of existing open hardware documentation standards (OKH, DIN SPEC 3105), or map to them? | assistant research, then owner | S-12, S-13 |
| Q-05 | Is the standard written in English only, or kept in step with a Japanese version? | owner | S-12 |
| Q-06 | When the operator is not the owner (staff, a contractor, a crew), how far can the owner delegate decisions within a run, and how is that delegation recorded? | owner | S-04, S-18 |
| Q-07 | What token budget should the status sheet of S-15 have? | measurement on the trial | S-15 |
