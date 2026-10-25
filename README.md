# Traceable Design

A working standard for designing physical things together with an AI assistant.
The aim is that anyone can trace every value and every decision in a design, long after the conversation that produced it is gone.

**Status: draft.**
Nothing here is stable yet.

## Why

An AI assistant can research, calculate, and write a complete design in a few days.
It can also produce a plausible number with no basis, lose track of what the owner decided, or let two documents drift apart.
This standard collects the rules that kept those failures in check on a real project, and turns them into something other makers can reuse.

## Layout

| Path | Content |
|------|---------|
| [spec/](spec/) | The standard itself, one chapter per file. |
| [notes/](notes/) | Raw material: what was done in practice, research, comparisons. |

## Passes

The standard is developed the way it asks a design to be developed.

1. Requirements of the standard: [spec/01-requirements.md](spec/01-requirements.md) (draft).
2. Form: the actors, the files of a record, the order of work, the tiers of change.
3. Rules and checks: each rule serves a requirement and says who or what checks it.
4. Template and checks taken out of the worked example, so a new project can start from them.
5. Trial on a small example and on a new project, judged against the design points of chapter 1.
6. The worked example moved onto the template.

## Worked example

[bread-oven](https://github.com/fujisato-koji/bread-oven) is a wood-fired bread oven designed this way (written in Japanese).

## License

- Code (tools, validators, scripts): MIT, see [LICENSE](LICENSE).
- Text (the standard, notes, documentation): CC BY 4.0, see [LICENSE-CC-BY-4.0.txt](LICENSE-CC-BY-4.0.txt).
