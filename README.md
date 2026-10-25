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

## Layout

| Path | Content |
|------|---------|
| [spec/](spec/) | The standard itself, one chapter per file. |
| [notes/](notes/) | Raw material: what was done in practice, research, comparisons. |

## Passes

The standard is developed the way it asks a design to be developed.

1. Requirements of the standard: [spec/01-requirements.md](spec/01-requirements.md) (draft).
2. Form: the actors, the files of a record, the phases of life and the order of work in each, the tiers of change: [spec/02-form.md](spec/02-form.md) (draft).
3. Rules and checks: each rule serves a requirement and says who or what checks it.
4. Template and checks taken out of the worked example, so a new project can start from them.
5. Trial on a small example and on a new project, judged against the design points of chapter 1.
6. The worked example moved onto the template.

## Worked example

[bread-oven](https://github.com/fujisato-koji/bread-oven) is a wood-fired bread oven designed this way (written in Japanese).

## License

- Code (tools, validators, scripts): MIT, see [LICENSE](LICENSE).
- Text (the standard, notes, documentation): CC BY 4.0, see [LICENSE-CC-BY-4.0.txt](LICENSE-CC-BY-4.0.txt).
