# 11. Offer conformance signals, never require them

- **Status:** accepted
- **Date:** 2026-10-18

## Context

The Baseline says nothing about how a project shows strangers that it conforms, yet trust
signals are the scope's top goal. The Best Practices Badge is a self-assessment form on a
third-party site, not something a project runs. Three things a project can run or keep
itself were researched ([research record](../research/2026-10-18-conformance-signals.md)):
a Security Insights file, the OSPS Baseline scanner, and OpenSSF Scorecard.

## Decision

- Record "nothing on showing conformance to strangers" as a gap in the skill's Baseline
  reference, with these three as candidate sources.
- Add a progressively loaded workflow for creating a Security Insights file: the agent
  fills in what the repository shows, asks the user for the rest, and shows a full preview
  (values and where each came from) for approval before writing anything.
- The skill does not mandate or add the OSPS Baseline scanner or Scorecard. On a
  GitHub-hosted repository the agent asks whether the user wants each one; on other hosts
  it does not offer them.

## Consequences

- Projects that opt in get public, repeatable signals; projects that do not are not
  penalised by the skill.
- Both tools are GitHub-only or GitHub-centred today; forge-neutral alternatives can be
  added if found.
