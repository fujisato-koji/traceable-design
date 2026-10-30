# Instructions for AI assistants working on this standard

This repository is the traceable-design standard itself, not the record of a thing.
The record of each thing lives in its own repository, started from [traceable-design/template](https://github.com/traceable-design/template) and owned by whoever makes the thing.

## Where things stand

Start from these, and read whole chapters only when a task needs them.

- `README.md`, section "Passes": which passes are drafted.
- `spec/decisions.md`: what the owner has decided about the standard.
- The open questions at the end of each chapter: 1.5, 2.9, and 3.10.
- Open pull requests: `gh pr list`.
- Trial in progress (pass 5): [fujisato-koji/drone](https://github.com/fujisato-koji/drone). Worked example, not yet moved onto the template (pass 6): [fujisato-koji/bread-oven](https://github.com/fujisato-koji/bread-oven).

## How to work

- Develop the standard the way it asks a design to be developed: requirements first, every rule traced to a requirement and to evidence in `notes/`, and every choice of the owner recorded in `spec/decisions.md`.
- One change per pull request, squash merged, and only when the owner says to merge.
- English, one sentence per line, no em or en dashes, no middle dots.
- Never add a number without its source, and say how far each source was read.
- Never write private facts of any project, such as where an owner lives or builds.
- After changing `tools/tdr.py` or the skill, run `python tools/sync_copies.py`, then `python tools/tests/test_tdr.py`. After changing `template/`, copy it to the template repository by hand (Q-14).
