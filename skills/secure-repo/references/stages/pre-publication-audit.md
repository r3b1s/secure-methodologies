# Audit before making a repository public

## When this applies

An existing repository, private until now, is about to be made public. Publishing exposes
its whole history and cannot be undone, so this is the most thorough stage.

## Before you start

- Find or start the [project record](../project-record.md): constraints, standing
  permissions (none by default) and the Baseline version (default: the one in
  [baseline.md](../baseline.md)).
- Agree a level with the human ([levels.md](../levels.md)).
- Frame the project from the README and the code, not from design documents
  (ground rule 3): what it does, who runs it, on what, with what privileges.

## Steps

1. **Check the history first.** Everything in it becomes public.
   - Scan the full history of every branch and tag for secrets
     ([tool categories](../tools/categories.md#secret-scanning)). Report locations, not
     values. A secret that was ever committed should be rotated, whether or not history is
     rewritten.
   - Review history for personal information: author and committer names and e-mail
     addresses, hostnames, home directory paths, internal URLs, names in test data.
   - List generated executables and unreviewable binaries in the tree and history
     ([OSPS-QA-05.01](../osps/level1/OSPS-QA-05.01.md), [OSPS-QA-05.02](../osps/level1/OSPS-QA-05.02.md)).
   - Present the findings. Whether to rewrite history, publish a fresh start, or accept
     what is there is the human's decision; rewriting must happen before publication.
2. **Get a tool baseline locally.** Propose the [tool categories](../tools/categories.md)
   that fit the project (at least SCA, SAST and CI/CD configuration analysis if it has
   pipelines), let the human choose the tools, and run them locally. Treat findings as
   candidates.
3. **Read the high-risk code in full.** Spend reading time in proportion to what could go
   wrong: code that runs with privilege, handles untrusted input (network, downloaded
   artifacts, files, environment), turns data into commands, paths or code, or handles
   secrets and downloads. Skim the rest through the tools, and say in the report which
   parts were only skimmed. When you find one instance of a problem, look for its siblings.
4. **Model threats and the risks of use** at the depth for the level
   ([threat-modeling.md](../threat-modeling.md)), even though the Baseline only requires
   this after a release.
5. **Assess every requirement at the project's level** using the
   requirement files for that level and every level below it
   ([level1/](../osps/level1/), [level2/](../osps/level2/), [level3/](../osps/level3/)),
   opening each file in turn and recording a
   status and how it was checked for each.
   Requirements that apply "after a release" are not applicable yet; note what would be
   needed at the first release.
6. **Check the gaps** listed in [baseline.md](../baseline.md#gaps-this-skill-fills):
   pinning, known-vulnerable dependencies, secure defaults, and how the project will show
   conformance (offer a [Security Insights file](../security-insights.md), and on GitHub
   the [tools to offer](../platforms/github.md#tools-to-offer)).
7. **Report and propose.** Report as ground rule 7 describes. Propose each fix separately,
   smallest first; make only the ones the human approves.
8. **Prepare the platform.** With approval, configure the settings the requirements need
   before going public (for example MFA, branch protection, private vulnerability
   reporting); see [platforms/](../platforms/).
9. **Go public.** Making the repository public is the human's action or explicit
   decision. Afterwards, confirm it is readable without signing in (OSPS-QA-01.01), and
   check the first runs of any CI.

## Human decision points

- the level, and any higher-level requirements to meet
- which tools to run
- what to do about history: rewrite, fresh start or accept
- each fix, and each accepted risk
- platform settings, and the moment of publication

## Done when

Every requirement at the level has a status with evidence; the history decision is made
and carried out; accepted risks are written where users will see them; the project record
is updated; and the human has decided to publish.
