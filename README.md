# Traceable Design

Systems engineering for working with an AI assistant, across the life of a physical thing: design, building, operation, change, and removal.
The aim is that anyone can trace every value and every decision about the thing, long after the conversations that produced them are gone.

**Status: draft.**
Nothing here is stable yet.

## Why

An AI assistant can research, calculate, and write a complete design in a few days.
It can also produce a plausible number with no basis, lose track of what the owner decided, or let two documents drift apart.
This standard collects the rules that kept those failures in check on a real project, and turns them into something other makers can reuse.

Systems engineering has long had the answers: numbered requirements, allocation, interface control, baselines, trade studies, verification plans.
Outside large programs it was rarely used, because people had to keep all that structure by hand.
With an assistant, the assistant keeps the structure, and the structure pays it back.
An assistant pays for every token it reads, on every turn, and most of its cost goes to re-reading.
A record built the systems engineering way lets it read only what a task needs.
So the same structure that makes a design accountable to people also makes it cheap for the assistant.
That is why systems engineering can now reach small projects, small firms, and individual makers.

## The state we aim for

Someone designs a thing, someone procures and makes its parts, someone builds it, and someone runs it.
What each of them learns always comes back: to the record of that thing, to the projects that follow, and to this standard.
Each new project starts from what the earlier ones verified, so everyone develops and runs things efficiently, and the standard keeps getting better from its use.

This is what putting AI to real use in the physical world means today.
An assistant cannot pick up a brick.
It reaches the physical world through the people who procure, make, build, and run things, and it learns about that world only from what they measure and report.
The record is the channel between them.
When the channel is precise and the loop closes, the assistant's work becomes things that stand and run; when it is not, the assistant designs blind.
Robots that can build in an open yard will take a long time, and when they come they will need the same record: exact values, procedures, and limits to work to, and a place to report what they measured.
So the record is not a stopgap until physical AI arrives; it is the layer physical AI will plug into.

## How it spreads

The standard is laid out in three layers, following what lasted in other fields ([notes/prior-art.md](notes/prior-art.md)).

1. **The standard**: plain files that any assistant can read and write, kept by a community and, once others adopt it, by a neutral body.
2. **Tools that pay off for one team alone**: an Agent Skill, an MCP server for looking up the record, a template, and checks. Nothing else is needed to benefit.
3. **Services on top**: a registry of shared items, the graph of who cites what, and notices when an item changes or is withdrawn. These come only after projects cite each other's items, and anyone may run them.

The first cluster is individual makers and makers near the owner.
First uses are sought where a receiver can ask for the format: a course that takes design work in it, and a maker who quotes from it.
Success is first measured by how many projects cite the same shared item.



| Path | Content |
|------|---------|
| [spec/](spec/) | The standard itself, one chapter per file, and [the decisions](spec/decisions.md) made about it. |
| [notes/](notes/) | Raw material: what was done in practice, research, comparisons. |
| [tools/](tools/) | [tdr.py](tools/tdr.py), the reference tool (checks, status sheet, lookup, briefs, change tiers, MCP server), and [usage_report.py](tools/usage_report.py), which shows where an assistant session spent its tokens. Python standard library only. |
| [skill/](skill/) | The Agent Skill an assistant follows: [skill/traceable-design/SKILL.md](skill/traceable-design/SKILL.md). |
| [template/](template/) | The starting layout of a new project's record, with the tool, the skill, and CI. |
| [examples/](examples/) | Small records used as test fixtures and as examples. |

## Passes

The standard is developed the way it asks a design to be developed.

1. Requirements of the standard: [spec/01-requirements.md](spec/01-requirements.md) (draft).
2. Form: the actors, the files of a record, the phases of life and the order of work in each, the tiers of change: [spec/02-form.md](spec/02-form.md) (draft).
3. Rules and checks: each rule serves a requirement and says who or what checks it: [spec/03-rules.md](spec/03-rules.md) (draft).
4. Template and checks taken out of the worked example, so a new project can start from them: [tools/tdr.py](tools/tdr.py), [skill/](skill/), [template/](template/) (draft).
5. Trial on a small example and on a new project, judged against the design points of chapter 1.
6. The worked example moved onto the template.
7. The first full loop: the worked example built and fired, and its findings returned to its own record and to this standard.

## Worked example

[bread-oven](https://github.com/fujisato-koji/bread-oven) is a wood-fired bread oven designed this way (written in Japanese).

## License

- Code (tools, validators, scripts): MIT, see [LICENSE](LICENSE).
- Text (the standard, notes, documentation): CC BY 4.0, see [LICENSE-CC-BY-4.0.txt](LICENSE-CC-BY-4.0.txt).
