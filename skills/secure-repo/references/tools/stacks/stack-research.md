# Researching an unfamiliar stack

Read this only when a repository's language, framework, package manager or build system
has no file in this folder, or when you are not confident you know the stack's current
security tooling and practices. The result is a set of options with sources for the human
to choose from, never a choice made for them (ground rule 1).

## Sources to trust, and how to verify them

Prefer, in this order:

1. **The stack's own official documentation**: the language, package manager or
   framework's documentation, security pages and advisory database.
2. **A tool's own repository and documentation**: its README, release notes, licence and
   issue tracker.
3. **Recognised security bodies** that publish openly: for example OpenSSF and OWASP.
4. **Everything else** (blog posts, articles, answers, search summaries) only to find
   leads, which you then confirm in the sources above.

For every fact you record:

- cite the page it came from, and the date you read it
- prefer the version-specific page (a tagged release, a versioned document) over a moving
  one
- if two sources disagree, say so, and say which you trust and why
- if you could not confirm it from a primary source, mark it unverified

Never state a tool fact from memory (ground rule 5). Tool landscapes change faster than
any model's training data.

## What to find out

For the stack in question:

- **Dependencies:** the standard package manager, its manifest and lock file formats, and
  how to install exactly what a lock file records.
- **Known vulnerabilities:** which advisory database covers the ecosystem, and which
  tools check dependencies against it.
- **Static analysis:** security-focused analysers and linters for the language, and what
  classes of weakness they cover.
- **Common weakness classes** for the language (for example memory safety, injection,
  unsafe deserialisation), so code reading knows where to look.
- **Build and release:** how artifacts are built and published, whether builds can be
  reproduced, and what signing or provenance the ecosystem's registry supports.
- **Tests:** the usual test runner, and whether fuzzing is practical for the language.

For each candidate tool, record: what it detects, what it misses, languages and versions
it supports, where it runs (locally, CI, hosted service), licence and cost, maintenance
status (latest release date, recent activity), and how it is installed.

## Recording what you found

Present the findings to the human as options with tradeoffs, grouped by the
[tool categories](../categories.md). If the human wants to keep them, write them up, with
their approval, as a stack file in this folder: one section per category, one entry per
tool with the fields above, the sources, and the date verified.

## What not to do

- Do not install, download or run anything found during research without the human's
  approval.
- Do not pick tools, versions or pipeline structure; present options (ground rule 1).
- Do not present search summaries or secondary sources as confirmed facts.
