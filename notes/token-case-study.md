# Token case study: the bread oven

This note measures where an AI assistant spent its tokens while designing the [bread-oven](https://github.com/fujisato-koji/bread-oven).
It is the evidence behind incident I-11 in [practice-inventory.md](practice-inventory.md) and requirement S-15 in [spec/01-requirements.md](../spec/01-requirements.md).

## What was measured

- One Claude Code session, from 2026-10-17 to 2026-10-22 (dates in UTC+9).
- The main conversation, 18 helpers it started, and 44 workflows with 239 agents that made calls.
- The work in that time: requirements, two changes of the first proposal, structural design, availability and prices, parts list, build schedule, firing procedure, a navigator with seven modes, and a thermal model.
- Measured with [tools/usage_report.py](../tools/usage_report.py), on 2026-10-25.

Each call's tokens are weighted by their price relative to one uncached input token: uncached input 1, cache write 1.25 (5 minutes) or 2 (1 hour), cache read 0.1, output 5.
The numbers below are shares of the weighted total, which was 473 million input-token equivalents over 16,169 calls.

## Results

### What the tokens paid for

| Component | Share |
|-----------|-------|
| Reading the context again (cache read) | 67.5 % |
| Writing the context into the cache | 25.5 % |
| Output (the assistant's writing and thinking) | 7.0 % |

More than nine tenths went to reading.

### Who spent them

| Scope | Share | Calls | Median context per call (tokens) |
|-------|-------|-------|----------------------------------|
| Workflow agents (239) | 76.5 % | 13,657 | 153,090 |
| Main conversation | 17.4 % | 1,007 | 475,053 |
| Helpers (18) | 6.1 % | 1,505 | 148,152 |

The main conversation's context reached 875,805 tokens at the 90th percentile and was compacted three times.

### When

| Day | Share | What happened |
|-----|-------|---------------|
| 2026-10-17 | 10.8 % | Requirements, first proposal |
| 2026-10-18 | 24.7 % | Prices and availability overturned the first proposal; the place, snow, and removal came in |
| 2026-10-19 | 28.6 % | Weight came in; a lighter, smaller oven was worked out |
| 2026-10-20 | 20.8 % | The new proposal was written into the repository; dome split and seams |
| 2026-10-21 | 12.5 % | Door stages, a front without a chimney, part visibility in 3D |
| 2026-10-22 | 2.4 % | Temperature contours in 3D |

The two days of rework after late requirements took 53 %.

### What filled the context

- Workflow agents each started empty and read the design from files.
  Their tool results came to about 39 million characters: shell commands 62 %, file reads 19 %, web search 13 %, web pages 6 %.
- Across all scopes, `sed`, `cat`, and `grep` returned 16.4 million characters, most of it parts of documents read through the shell.
- The working specification of the new proposal, kept outside the repository while it was drafted, was read 89 times for 1.16 million characters.
- The largest documents were read about 60 times each: the structural design (2,059 lines) and the 3D viewer's code (3,590 lines).
- Screen checks took 605 screenshots.

## Reading it with systems engineering

| What happened | Systems engineering tool | Effect for the assistant |
|---------------|-------------------------|--------------------------|
| Rework after late requirements took half the tokens. | Stakeholder needs analysis; early checks of availability and cost | Fewer rounds of rework |
| Every agent re-read the whole design. | Allocation of requirements; interface control | A helper gets its part and the part's interfaces only |
| The main conversation carried its history on every turn. | Baselines; configuration management; phase gates | End the conversation at a gate and start the next from one status sheet |
| Values were found by reading documents through the shell. | A model that can be queried | An id returns the value and its basis in one line |
| Checks were done by agents reading, with screenshots. | A verification plan | Scripts check what they can at almost no token cost; agents take only claims that need judgment |
| Options were compared again in several workflows. | Recorded trade studies | Settled choices are not reopened |

## A rough estimate

If workflow agents started from a brief with the ids and files they need and a status sheet, instead of the full documents, their median context might fall from about 150 thousand to about 50 thousand tokens.
That would cut their reading share from 53 % to about 18 %, saving about a third of the total.
Keeping the main conversation under 200 thousand tokens by ending it at gates would cut its reading share from 10 % to about 4 %.
Together, about 40 % of the total.
Rework avoided by asking the right questions early is not counted.
This is an estimate to be tested on the next project, against the expected value of S-15.

## Limits

- One session, one project, one assistant, one person.
- Weights follow list prices; usage limits on a subscription may weigh the components differently.
- Characters of tool results are not tokens; they show where the context came from, not its exact cost.
- There is no control: the same design was not done another way to compare.
