# Tool categories

> Categories only. Specific tools belong in [stacks/](stacks/) and are suggestions, never
> requirements; choosing a tool is the human's decision (ground rule 1).

Deterministic tools cover the whole codebase the same way every time, so they find what
reading misses. They also produce false positives and miss whole classes of problems, so
a clean run proves nothing on its own (ground rule 4). Run them locally first, so that any
CI added later reproduces a state you already understand.

## How to read an entry

Each category says what it finds, what it misses, where it usually runs, and which
Baseline requirements or gaps it supports. Entries for specific tools, in stack files,
also record: languages, licence and cost, maintenance status, and the date the entry was
last verified against the tool's own documentation.

## Categories

### Secret scanning

- **Finds:** credentials, keys and tokens in files and in the full history.
- **Misses:** secret formats it does not know, encoded or split secrets, and personal
  information (names, e-mail addresses, hostnames, home paths), which needs a separate
  review.
- **Runs:** locally, as a pre-commit hook, in CI, or as a platform feature.
- **Supports:** OSPS-BR-07.01; the "leaks other than secrets" gap needs more than this.

### Software composition analysis (SCA)

- **Finds:** dependencies with known vulnerabilities, known-malicious packages, and
  licence issues, matched against advisory databases.
- **Misses:** vulnerabilities not yet published, and code copied into the repository
  without being declared as a dependency. Results are only as complete as the manifest or
  lock file it reads.
- **Runs:** locally or in CI, against manifests, lock files or a built environment.
- **Supports:** OSPS-VM-05.01 to 05.03; the "known-vulnerable dependencies" gap.

### Static application security testing (SAST)

- **Finds:** code patterns associated with weaknesses (injection, unsafe deserialisation,
  path handling, weak cryptography), sometimes by tracing data from sources to sinks.
- **Misses:** flaws in design and logic, and anything that depends on context it cannot
  see; produces false positives that need judgement.
- **Runs:** locally or in CI.
- **Supports:** OSPS-VM-06.01 and 06.02; the "security of the code itself" gap.

### Linting and type checking

- **Finds:** defects and risky constructs at the language level; some linters include
  security rules.
- **Misses:** most security issues beyond local patterns.
- **Runs:** locally, in editors, in CI.
- **Supports:** code quality where it affects security; contribution requirements
  (OSPS-GV-03.02).

### CI/CD configuration analysis

- **Finds:** injection of untrusted input into pipeline scripts, excessive token
  permissions, risky triggers, and third-party pipeline components not pinned to an
  immutable reference.
- **Misses:** problems in scripts the pipeline calls, and platform settings outside the
  configuration files.
- **Runs:** locally or in CI, against pipeline definitions.
- **Supports:** OSPS-AC-04.01 and 04.02, OSPS-BR-01.01, 01.03 and 01.04; the "pinning" gap.

### Dependency pinning and update automation

- **Finds:** outdated pinned versions, and proposes updates.
- **Misses:** whether an update is safe; updates still need review.
- **Runs:** as a scheduled service or bot on the platform, or locally.
- **Supports:** the "pinning" gap; OSPS-DO-06.01 (describing how dependencies are tracked).

### Infrastructure-as-code and container scanning

- **Finds:** misconfiguration in container definitions, deployment manifests and
  infrastructure code, and known vulnerabilities in container images.
- **Misses:** runtime behaviour. Only relevant if the project ships such files or images.
- **Runs:** locally or in CI.
- **Supports:** the "security of the code itself" gap; secure defaults.

### SBOM generation

- **Finds:** nothing; it records which components a build contains.
- **Misses:** components the generator cannot see (vendored or dynamically fetched code);
  accuracy varies, so check its output.
- **Runs:** at build time.
- **Supports:** OSPS-QA-02.02.

### Signing and provenance

- **Finds:** nothing; it lets users verify where and how a release was built and that it
  was not altered.
- **Misses:** whether the source itself was trustworthy.
- **Runs:** at release time, in the release pipeline.
- **Supports:** OSPS-BR-06.01, OSPS-DO-03.01 and 03.02.

### Fuzzing

- **Finds:** crashes, hangs and memory errors from unexpected input, especially in parsers
  and decoders.
- **Misses:** anything its harnesses do not reach; needs harnesses written per entry point.
- **Runs:** locally or on continuous fuzzing infrastructure.
- **Supports:** the "security of the code itself" gap, for code that handles untrusted
  input.

### Dynamic application security testing (DAST)

- **Finds:** vulnerabilities in a running application through its external interfaces.
- **Misses:** code paths it does not exercise. Only relevant to software that exposes a
  network service or similar interface.
- **Runs:** against a running test deployment.
- **Supports:** the "security of the code itself" gap.

### Repository posture and Baseline assessment

- **Finds:** platform settings and practices (branch protection, token permissions,
  security policy, pinning), and, for Baseline scanners, a verdict per requirement.
- **Misses:** anything it cannot see through the platform's API; some results need manual
  review.
- **Runs:** in CI or from a command line against the hosted repository. Tools in this
  category are usually tied to one platform.
- **Supports:** the "showing conformance to strangers" gap; checking many AC, QA and VM
  requirements.

### Automated tests

- **Finds:** regressions in the behaviour the tests cover, including security fixes once a
  test exists for them.
- **Misses:** everything untested.
- **Runs:** locally and in CI.
- **Supports:** OSPS-QA-06.01 to 06.03.
