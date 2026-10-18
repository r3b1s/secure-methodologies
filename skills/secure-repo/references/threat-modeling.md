# Threat modelling and the risks of using a project

> Sources checked 2026-10-18.

## What the Baseline requires

After a release: design documentation of actors and actions (OSPS-SA-01.01, level 2),
descriptions of external interfaces (OSPS-SA-02.01, level 2), a security assessment of the
likeliest and most damaging problems (OSPS-SA-03.01, level 2), and threat modelling with
attack-surface analysis (OSPS-SA-03.02, level 3). See
[OSPS-SA-01.01](osps/level2/OSPS-SA-01.01.md), [OSPS-SA-02.01](osps/level2/OSPS-SA-02.01.md), [OSPS-SA-03.01](osps/level2/OSPS-SA-03.01.md), [OSPS-SA-03.02](osps/level3/OSPS-SA-03.02.md).

This skill goes further in two ways:

- **Before the first release too.** Publishing a repository already exposes its code and
  its users to risk, so assess it before it goes public, at a depth suited to its level.
- **Telling users.** The Baseline requires the assessment to be performed, not shared.
  This skill also records, where users will read it, the risks they accept by using the
  software.

## Depth by level

| Situation | Depth |
|---|---|
| Level 1, or before a first release | a short model and a list of what can go wrong at each trust boundary, with responses |
| Level 2 | a written security assessment covering the likeliest and most damaging problems |
| Level 3 | a full threat model and attack-surface analysis of critical code paths |

Raise the depth when the software runs with privilege, is exposed to a network or handles
untrusted input (see [levels.md](levels.md)).

## How to do it

Use the four questions of the [Threat Modeling Manifesto](https://www.threatmodelingmanifesto.org/),
which the [OWASP Threat Modeling Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Threat_Modeling_Cheat_Sheet.html)
also builds on. Work from the code, not from existing design documents (ground rule 3).

### 1. What are we working on?

Model the system as it is built and as users run it:

- components, data stores and external entities (users, services, other software)
- data flows between them, and the **trust boundaries** those flows cross (for example
  user to root, network to process, downloaded file to parser)
- how it is installed, deployed and run, and with what privileges
- what it downloads, executes or trusts (dependencies, artifacts, update channels)

A data-flow diagram is the most common form; a written list is enough at level 1.

### 2. What can go wrong?

Walk each trust boundary and data flow. The STRIDE categories (Spoofing, Tampering,
Repudiation, Information disclosure, Denial of service, Elevation of privilege) are useful
prompts. At each boundary ask who controls the data and who acts on it, with what
privilege: data that merely sits in a trusted place is not trusted data. Include the
supply chain (dependencies, build, distribution) and secrets.

### 3. What are we going to do about it?

Give each threat one response: mitigate, eliminate (remove the feature), transfer (to
another party, documenting what remains), or accept. Changing behaviour and accepting a
risk are the human's decisions (ground rule 1).

### 4. Did we do a good enough job?

Check the model against the code, confirm every threat has an agreed response, and have
the human review it. Record the result and its date in the [project record](project-record.md).

## Secure defaults

The Baseline asks for visible warnings on dangerous actions (OSPS-DO-01.01) but not for
secure defaults. Check what the software does out of the box: what it exposes, what it
trusts, what permissions it sets, and whether a safer default exists. CISA's
[Secure by Design](https://www.cisa.gov/securebydesign) principles call for products to be
secure out of the box. Propose safer defaults, or document the risk; either is the human's
decision.

## Recording the risks a user accepts

Publish a short security model where users will find it (for example a section of the
security policy or the README). It covers:

- what the software does with privilege, and why (an enumerated list)
- what it trusts, and what it does not protect against
- each accepted risk, with the reason it is accepted and any mitigation
- how a cautious user can reduce their exposure (for example a preview or dry-run mode)

Every statement must be checkable against the code. An accepted risk that users are not
told about is an unknown risk to them.
