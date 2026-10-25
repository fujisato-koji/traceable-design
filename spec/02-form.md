# 2. Form of the standard

This chapter is the second pass.
It chooses the overall shape of the standard: who does what, where each kind of fact lives, how the assistant reads, how the life of the thing is divided, how changes are sorted, and who checks what.
The detailed rules, file formats, and checks come in chapter 3 and must follow the choices made here.

Each choice cites the requirements of [chapter 1](01-requirements.md) it serves.
Evidence marks (C-nn, I-nn) point to [notes/practice-inventory.md](../notes/practice-inventory.md).
Every selection in this chapter is a recommendation until the owner decides it.

## 2.1 What the form must settle

| ID | Choice | Requirements it answers |
|----|--------|-------------------------|
| F-1 | Actors and their authority | S-04, S-05, S-06, S-12 |
| F-2 | Where each kind of fact lives | S-01, S-07, S-12, S-13, S-15 |
| F-3 | How the assistant reads: status sheet, lookup by id, briefs | S-09, S-15 |
| F-4 | Phases of life, the order of work in each, and the gates between them | S-08, S-10, S-16, S-17, S-18 |
| F-5 | Tiers of change | S-06, S-11 |
| F-6 | Who or what checks each thing | S-03, S-06, S-07, S-17 |
| F-7 | Where private facts live | S-09, S-14 |

## 2.2 F-1 Actors and authority

| Actor | May | May not |
|-------|-----|---------|
| Owner | Decide requirements, limits, deadlines, options, budgets, and anything hard to undo. Approve a change into the record. | (nothing is withheld) |
| Operator | Run the thing within the limits and procedures the owner set. Stop a run. | Change a limit or a procedure. Resume after a limit was reached, unless the owner delegated that (Q-06). |
| Lead assistant | Write the record. Propose options with a recommendation. Start helpers and checkers. Advise during a run. | Decide anything in the owner's column. Relax a limit, a deadline, or a margin. |
| Helper | Do one task from a brief and write its result on its own branch or in a result file. | Widen its task beyond the brief. Decide. |
| Checker | Check a claim or a change independently and report findings. | Edit the claim it checks, for changes of tier T2 or T3 (2.6). |

A person, a script, or an assistant session can be a checker.
The owner and the operator are often the same person in a personal project, and the standard does not ask them to be different.

The line between helper and checker comes from practice.
For speed, a checker in the worked example fixed what it found on the spot (I-05).
That is kept for small changes, but a checker that rewrites the claim it is checking is no longer independent of it (S-06), so for new claims the checker reports and a helper fixes.

## 2.3 F-2 Where each kind of fact lives

### Candidates

| Candidate | Shape |
|-----------|-------|
| A. Documents first | The record is prose documents; scripts parse tables out of them. This is mostly how the worked example started (C-04). |
| B. Data first | Every fact is in data files; documents are generated whole. |
| C. Split by kind | Facts that a machine checks or looks up live in data files. Reasoning lives in prose documents that cite ids. Tables inside prose are generated from data between markers (C-16). |

### Comparison

| Yardstick | A | B | C |
|-----------|---|---|---|
| S-01, S-07: a machine can check every value and reference | fair: parsers grow with each new table (C-04, C-14) | good | good |
| S-15: a value can be looked up without reading a document | poor: the value sits inside prose | good | good |
| Reasoning can be read and reviewed by people | good | poor: reasoning inside data strings | good |
| S-12: the owner never edits files by hand | good | good | good |
| S-13: plain files and plain scripts | good | good | good |
| Cost to set up | low | high: every document needs a generator | medium: generators only for tables |

### Selection

C, split by kind.
The worked example already uses it for dimensions, parts, steps, and items (C-21), but keeps requirements, sources, decisions, and open items in prose.
Under C those move into data as well, because they are exactly what the assistant needs to look up.

### Kinds of fact and their home

| Kind | Id form | Holds | Lives in |
|------|---------|-------|----------|
| Requirement | R-nn, R-nna | text, origin, design point, expected value, verification method, basis, status, parent, allocated parts | data |
| Value | dotted key (`dome.thickness`) | value, unit, status, basis | data |
| Source | P-nn, S-nn, M-nn, F-nn | class, bibliography, URL, retrieval date, license, how far it was read | data |
| Decision | D-nnn | date, who, what was decided, options considered, ids it touches, what it supersedes | data |
| Open item | Q-nnn | question or finding, waits for, affects, opened, closed by (a decision id) | data |
| Hazard | H-nn | hazard, phases, people or property at risk, controls (requirement ids, procedure step ids) | data |
| Part and interface | part id; interface id | parts, and what crosses between two parts (load, heat, gas, signal) | data |
| Check | K-nnn | claim or change checked, method, result, date, by whom | data |
| Configuration | baseline id | as designed, as built (each deviation: key, design value, built value, decision), as operated now | data |
| Run | run id | date, public conditions, measured values by key, deviations, findings | data |
| Procedure step | step id | action, values by key, hazard controls by id, limits | data, rendered as a document |
| Status sheet | (one per record) | phase, configuration in force, recent decisions, open items, next steps | generated |
| Reasoning | section ids | why: comparisons, calculations, readings of sources, each citing ids | prose |

The interface kind is new compared with the worked example.
It is what lets a helper take one part and only the parts that touch it (F-3).

## 2.4 F-3 How the assistant reads

### Candidates

| Candidate | Shape |
|-----------|-------|
| A. A summary written by hand | One summary document, kept up to date by the assistant, read at the start of each session. |
| B. Generated status sheet, lookup by id, generated briefs | A script writes the status sheet from the data. Another answers an id with the item and its basis in a few lines. A brief for a helper is assembled from the ids its task needs. |
| C. Search over the documents | An index of the documents answers questions by similarity. |

### Comparison

| Yardstick | A | B | C |
|-----------|---|---|---|
| S-15: small and predictable reading | fair: grows without limit | good: size set by the generator | fair: returns passages, not facts |
| S-01: what is read carries its basis | poor: a summary drops the basis | good | poor |
| S-07: cannot drift from the record | poor: a second copy of the facts | good: generated | good |
| S-13: no service, no network | good | good | poor: needs an index and usually an embedding service |
| Needs the data-first split of F-2 | no | yes | no |

### Selection

B.
It needs F-2 C, which is selected.
Its parts:

- **Status sheet.** Generated from the data on every change, with a budget in tokens.
  It is the first and often the only thing a new session reads (S-09).
  The budget is open (Q-07); a starting point is a design point of 10,000 tokens and an expected value of 5,000.
- **Lookup.** One command takes an id or a value key and returns the item, its status, and its basis, and another returns what refers to it.
  The assistant looks values up instead of reading documents through the shell, which in the worked example returned millions of characters (I-11).
- **Brief.** One command takes a task's ids (a part, a requirement, an open item) and assembles what the task needs: the items, their requirements and values, the interfaces of the parts, the open items that touch them, and the sections of reasoning by id.
  A helper starts from its brief, not from the documents.
- **Gates for the conversation.** The lead conversation ends at each gate of F-4, or when its context passes a set size, and the next one starts from the status sheet.
  In the worked example, the main conversation carried a median context of nearly half a million tokens on every turn (I-11).

## 2.5 F-4 Phases, order of work, and gates

### Phases

| Phase | Work in order | Stage of ISO/IEC/IEEE 15288 |
|-------|---------------|-----------------------------|
| 1. Design | 1.1 requirements, 1.2 form, 1.3 design calculation, 1.4 availability, 1.5 parts and cost | concept, development |
| 2. Build | building, recording as built | production |
| 3. Operate | runs; inspection and maintenance | utilization, support |
| 4. Change | re-enter the stage that owns the changed item | (any) |
| 5. Remove | removal procedure, closing the record | retirement |

### The questions that kill forms come first

In the worked example, the place, the snow, the weight, the removal, and the real prices arrived after a form was chosen.
The two days of rework they caused were the costliest of the project (I-06, I-11).
So step 1.1 starts with a fixed list of questions that can rule a form out, asked before any form is compared:

- where the thing stands, and its climate (frost, snow, wind)
- the budget, and what it includes
- which materials and services can be had at that place, at what price
- weight, size, and whether it must be moved or removed
- the skills, tools, and help the builder has
- when it must be ready, and how often it will be used
- laws, permits, and neighbors

A rough check of availability and cost is done for each candidate form in step 1.2, before the full step 1.4.

### Gates

| Gate | Passed when | Decided by |
|------|-------------|------------|
| Design to build | Every requirement has a design value and a verification method. Every hazard has a control. Open items that block building are closed. The parts list is priced. | owner |
| Build to operate | The as-built configuration is recorded. Each design point has a first-use check. Procedures are generated and their values resolve. | owner |
| Each run | Before: the procedure's checks and limits. After: the run log, and the comparison of measured with predicted values. | operator, then owner for findings |
| Change | The change's tier is set and its checks pass. | owner for T2 and T3 |
| Remove | The removal procedure and its hazards are recorded. | owner |

The lead conversation ends at each gate (F-3).

## 2.6 F-5 Tiers of change

| Tier | What changes | Checks | Owner |
|------|--------------|--------|-------|
| T0 Record | Wording, links, layout, or writing down a decision already made | Scripts | No further step |
| T1 Value | A value changes on a basis already in the record (the same checked model, a newer price from the same shop) | Scripts. A checker may fix what it finds. | Sees the change if it touches a design point or a budget |
| T2 Claim | A new calculation, model, or source that a decision will rest on | Scripts, then an independent check. The checker reports; a helper fixes. | Decides after the check |
| T3 Limit | A requirement, a limit, a hazard control, or the configuration of something built or running | As T2, plus a review of hazards that the change touches | Decides; never during a run |

Every change states its tier.
A script refuses a T2 change without a check record and a T3 change without a decision id.
In the worked example, writing decisions and rewording went through the same full process as new calculations, which the owner found too slow (I-05).

## 2.7 F-6 Who or what checks each thing

| What | Checked by | When |
|------|------------|------|
| References, ids, generated tables, status and basis present, sums, schedule order, private names | scripts | every change |
| Values in documents against models | scripts | every change |
| New claims a decision rests on | an independent checker, given the claim and its inputs by id | before the owner decides |
| Decisions | the owner, from a report that shows current and proposed side by side | at the decision |
| Design points | inspection, analysis, demonstration, or test, as the requirement's verification method says | design, then first use |
| Model predictions | measurements from runs | after each run |

Each requirement carries a verification method, one of inspection, analysis, demonstration, and test.
The worked example named its checks in prose (C-13); here they become records (K-nnn) that a script can count.

## 2.8 F-7 Private facts

Private facts (the place, the station, the address, local conditions that point to a place) live in a private store outside the public record, with the same ids.
The public record keeps the derived values, and marks the basis of each as coming from a private fact.
The list of private names lives in the private store, and the check of S-14 reads it from there, locally or from a secret in CI.
Run logs follow the same split (1.4 of chapter 1).

## 2.9 Open items

| No. | Question | Waits for | Affects |
|-----|----------|-----------|---------|
| Q-07 | The token budget of the status sheet (carried from chapter 1). | measurement on the trial | F-3 |
| Q-08 | The format of data files: YAML with a strict subset (no flow style, after the comma accident behind E17), JSON, or TOML. | chapter 3 | F-2 |
| Q-09 | Whether the lookup and brief commands are part of the standard, or only an example of how to meet it. | owner | F-3, S-13 |
| Q-10 | How the worked example moves its requirements, sources, decisions, and open items from prose into data. | pass 6 | F-2 |

## 2.10 Reflect to

| Where | What |
|-------|------|
| Chapter 3 | One schema per kind of fact in 2.3; the status sheet, lookup, and brief commands; the tier check; the deny-list check; the verification records. |
| Chapter 1 | S-15's status sheet and S-16's configurations are defined here. |
| README | Passes: chapter 2 is drafted. |
