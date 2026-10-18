# The project record

Every stage reads and updates one record of where the project stands. It is what makes
later work repeatable: a re-audit starts from it, and an agent's standing permissions only
count if they are written in it (ground rule 2).

## What it holds

| Section | Contents |
|---|---|
| Baseline | the version the project is assessed against, and the date of the last assessment |
| Level | the level targeted, any requirements from higher levels the project has chosen to meet as well, and why |
| Constraints | what CI can and cannot run (and why), tools that are acceptable or ruled out, hosting, anything else that limits the work |
| Standing permissions | kinds of change an agent may make without asking each time, named precisely; empty by default |
| Results | for each requirement at the project's level: status (met, not met, not applicable, not checked), how it was checked, and the date |
| Accepted risks | each risk the human accepted, with the reason; users are told about it in the README's security model section |
| Open items | requirements not yet met and gaps found, with what was decided about each |

## Where it lives

Ask the human. Unless they prefer otherwise, suggest a Markdown file in the project's own
repository, so it is versioned with the code and visible to reviewers. A public record of
results is also a trust signal; if the project has a Security Insights file, its
self-assessment can link to it.

If the human wants parts kept private (for example standing permissions for agents), keep
those parts wherever they choose and note in the public record that they exist.

## Rules

- Create or change the record only with the human's approval (ground rule 2).
- Never record a status without saying how it was checked.
- Do not change results because a new Baseline version exists; see
  [baseline-upgrade.md](baseline-upgrade.md).
