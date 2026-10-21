# 19. Add a skill for the qubesadmin Python library

- **Status:** accepted
- **Date:** 2026-10-21
- **Amends:** [0017](0017-add-qubes-os-skills.md)

## Context

[0017](0017-add-qubes-os-skills.md) added three Qubes OS skills about command-line tools
and disposable qubes, and requires a new record for further topics. The owner is moving
their Qubes OS configuration from imperative dom0 shell scripts towards declarative
management that can run from a management qube instead of dom0. On Qubes OS R4.3 the
supported route for that is the Admin API, through `qubesadmin`, the Python library the
`qvm-*` tools are built on. Upstream ships it as `qubes-core-admin-client`, but in code it
is a library wrapping the API rather than a separate client, and the skill names it so.

Upstream documentation describes the Admin API's calls and the `qvm-*` tools, but not the
library: how it reaches `qubesd` (a local socket in dom0, which bypasses qrexec policy,
and policy-checked qrexec elsewhere), which calls each operation makes, how it reports
policy denials, or how to test code against it. These were read from the library and
server source (`qubes-core-admin-client` 4.3.35, `qubes-core-admin` 4.3.53) on
2026-10-21.

## Decision

- Add `qubes-admin-python` to the `qubes-os` category: writing Python against
  `qubesadmin` for provisioning, declarative configuration management and event-driven
  automation, from dom0 or a management qube, including the qrexec policy that scopes
  such code.
- The skill includes a working example, `assets/reconcile.py`, with offline tests that
  use the library's own `QubesTest` fake, so the example's behaviour and its exact Admin
  API calls are checked without a Qubes system.
- It follows the same rules as the other Qubes OS skills: self-contained
  ([0010](0010-skills-self-contained.md)), MIT licensed, grounded in primary sources, and
  stating what it was checked against. Unlike the other three it was checked against
  source and an offline fake, not a live R4.3.2 install, and says so.

## Consequences

- The `qubes-os` category has four skills; installing the category installs all four.
- The skill tracks the library's Python API, which upstream does not promise to keep
  stable across releases (R4.3 replaced the device API), so it needs re-checking at each
  Qubes OS release alongside the other Qubes OS skills.
- Its claims should be confirmed on a live system when one is available, and the
  `verified-on` field updated then.
