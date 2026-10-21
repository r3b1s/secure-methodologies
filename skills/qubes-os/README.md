# Qubes OS skills

[Agent Skills](https://agentskills.io/) for working with
[Qubes OS](https://www.qubes-os.org/): running commands in the right place, and
building qubes whose configuration and secrets end up where they should.

This folder is a category, not a skill: it has no `SKILL.md`, and each subfolder is one
self-contained skill.

| Skill | Use it when |
|---|---|
| [qubes-dom0-cli](qubes-dom0-cli/SKILL.md) | Running anything in dom0: `qvm-*` lifecycle, properties, features, firewall, devices, storage, templates, backups, updates, and qrexec policy. |
| [qubes-vm-cli](qubes-vm-cli/SKILL.md) | Working inside a qube that is not dom0: moving files, calling services in other qubes, reading the qube's own configuration, debugging denied qrexec calls. |
| [qubes-disposable-vms](qubes-disposable-vms/SKILL.md) | Building disposables and named disposables (e.g. `sys-*` service qubes): what persists where, stateful services, bind-dirs, boot hooks, and dom0 provisioning scripts. |
| [qubes-admin-python](qubes-admin-python/SKILL.md) | Writing Python against `qubesadmin`, the library over the Admin API: provisioning and declarative config management from dom0 or a management qube, idempotent read-compare-write, events, offline tests with `QubesTest`, and the qrexec policy that scopes it. |

The command references were checked against Qubes OS R4.3.2 and upstream documentation at
[QubesOS/qubes-doc](https://github.com/QubesOS/qubes-doc). `qubes-admin-python` was
checked against the R4.3 library and server source, and its example against the library's
offline test fake, not a live install. Where an installed tool or upstream disagrees with
a skill, they win.

## Installing

With the [`skills` CLI](https://github.com/vercel-labs/skills):

```sh
npx skills add r3b1s/secure-methodologies/skills/qubes-os          # all Qubes OS skills
npx skills add r3b1s/secure-methodologies --skill qubes-dom0-cli    # one skill
```

Add `-g` to install for your user rather than the current project. Skills install by
name, without this category folder (for example `.claude/skills/qubes-dom0-cli/`).
