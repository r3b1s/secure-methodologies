# 16. Publish the security model as a section of the README

- **Status:** accepted
- **Date:** 2026-10-18

## Context

The skill's threat modelling guidance asks projects to publish the risks users accept, and
had suggested the security policy or the README as the place. [0015](0015-security-md-template.md)
defined SECURITY.md narrowly as the vulnerability disclosure policy, so the security model
does not belong there. A Security Insights file holds short structured declarations; it
has fields for scope and for a link to a self-assessment, but none for the explanation
itself.

## Decision

For now, a project's security model is an easily visible section of its README that
explains the threat model and the risks of using the software. `SECURITY.md` may link to
it to explain what counts as a vulnerability, and a Security Insights file may link to it
from `security.assessments.self.evidence`. The term is defined in the
[glossary](../glossary.md#security-model).

## Consequences

- Users meet the risks where they first read about the project, before installing it.
- A long security model can make the README unwieldy; moving it to its own document,
  linked from the README, is an option for a later iteration.
