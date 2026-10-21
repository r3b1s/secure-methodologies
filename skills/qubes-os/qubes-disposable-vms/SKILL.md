---
name: qubes-disposable-vms
description: Patterns for building disposable qubes on Qubes OS 4.2+ — disposable templates, named disposables as service qubes (sys-*), where packages, config, state and secrets must live so they persist, and idempotent dom0 provisioning. Use when creating or debugging a disposable or named disposable, when settings or logins "don't survive a reboot" of a disposable, when adding bind-dirs/rc.local/firewall rules to one, or when writing a dom0 script that provisions qubes.
license: MIT
---

# Qubes disposable qubes

Sources of truth: these pages of https://github.com/QubesOS/qubes-doc
(rendered at https://doc.qubes-os.org/):
`user/how-to-guides/how-to-use-disposables.rst`,
`user/advanced-topics/disposable-customization.rst`,
`user/advanced-topics/bind-dirs.rst`, `user/advanced-topics/config-files.rst`
and `user/security-in-qubes/firewall.rst`. When this file and upstream
disagree, upstream wins.

## 1. The persistence model (get this right first)

A disposable is assembled from three qubes. Every "it didn't persist" bug is
a write landing in the wrong one.

| Layer | Class | Volume that matters | Persists? | Put here |
|---|---|---|---|---|
| **TemplateVM** (e.g. `tpl-foo`) | `TemplateVM` | root (`/usr`, `/etc`, `/var` outside bind-dirs) | Yes, committed at **template shutdown** | Packages, systemd units and drop-ins, helper scripts in `/usr/bin` |
| **Disposable template** (e.g. `dvm-foo`) | `AppVM` + `template_for_dispvms=True` | private (`/rw`, `/home`) | Yes, committed at **dvm-template shutdown** | `/rw/config/*` hooks, bind-dirs config and data, anything every disposable should start with |
| **Disposable / named disposable** (e.g. `sys-foo`) | `DispVM` | none | **No.** Root and `/rw` are fresh copies at every start; everything is discarded at shutdown, bind-dirs included | Nothing. Runtime only |

Consequences:

- **A disposable starts from the dvm template's last *committed* `/rw`.**
  Writes to a running dvm template are invisible to disposables until the
  dvm template shuts down. Order is always: write → `qvm-shutdown --wait
  dvm-foo` → start the disposable.
- **Template root changes need two restarts:** shut down the TemplateVM to
  commit, then restart the dvm template and the disposable to pick it up.
- **bind-dirs in a disposable do not persist.** They redirect writes into
  `/rw`, but a disposable's `/rw` is itself thrown away. bind-dirs only help
  when the *dvm template* writes the data.
- **Per-instance values go in `vm-config.*` features, not shared state:**
  `qvm-features sys-foo vm-config.<key> <value>` in dom0, read inside with
  `qubesdb-read /vm-config/<key>`. That avoids writing a file into the dvm
  template and cycling it.

## 2. Stateful service in a disposable (logins, keys, enrollment)

To have a VPN, mesh, or other enrolled client come up already logged in in a
named disposable:

1. Bind-dir the daemon's state directory in the **dvm template**
   (`/rw/config/qubes-bind-dirs.d/50_<name>.conf`), then shut it down so the
   bind is active on its next boot.
2. **Enroll inside the dvm template**, not the disposable: start it, run the
   login/enroll command there, confirm it works, `qvm-shutdown --wait` it.
3. Start the named disposable. It inherits the committed state and is logged
   in on every boot. Anything the daemon writes later is discarded, which is
   usually what you want.

Rules that come with this:

- **Everything in the dvm template's `/rw` is shared by every disposable
  spawned from it**, secrets and identities included. Use one dvm template
  per identity. Never make it a `default_dispvm`, and keep
  `appmenus-dispvm` unset so nobody launches extra copies of the identity.
- **Never run the dvm template and its named disposable at the same time**
  when they hold a network identity: two peers with one key fight over it.
  Provisioning scripts should shut both down first.
- Enroll with non-interactive credentials (setup keys, tokens through stdin).
  A browser or SSO flow inside a service qube stalls provisioning.

## 3. bind-dirs semantics

- Config: `/rw/config/qubes-bind-dirs.d/50_<name>.conf` containing
  `binds+=( '/var/lib/foo' )`.
- At boot, bind-dirs **copies the original into `/rw/bind-dirs/...` only if
  that path does not exist yet**, then bind-mounts it over the original.
- Pre-creating an empty `/rw/bind-dirs/var/lib/foo` therefore *hides* the
  template's content. Do it deliberately (e.g. to avoid inheriting a key or
  profile that a package's postinst generated in the template), or let
  bind-dirs create it.
- Takes effect on the next boot of the qube that owns the `/rw`.

## 4. Startup hooks and ordering

All of these live in the dvm template's `/rw/config/` (`config-files.rst`):

| Hook | Runs | Use for |
|---|---|---|
| `rc.local-early`, `rc.local-early.d/*.rc` | before `sysinit.target`, before network setup | Things that must exist before any interface is up |
| `rc.local.d/*.rc`, then `rc.local` | at startup, **after the network is up** (run by `qubes-misc-post.service`) | General per-boot setup. Upstream warns: not for leak-blocking rules |
| `qubes-firewall.d/*`, `qubes-firewall-user-script` | in qubes with the `qubes-firewall` service (net-providing qubes) at firewall start | Forward and leak-prevention rules for downstream qubes |

All of them must be executable (`chmod 0755`). If a daemon from the template
must not start before your `rc.local` rules exist, order it with a drop-in in
the **TemplateVM**: `/etc/systemd/system/<unit>.service.d/10-qubes-order.conf`
containing `[Unit]` / `After=qubes-misc-post.service`.

## 5. Services and features

- `qvm-service sys-foo <name> on` sets feature `service.<name>`, which shows up
  inside as `/var/run/qubes-service/<name>`. Gate template units on it with
  `ConditionPathExists=/var/run/qubes-service/<name>`, so one template can
  serve qubes that should and should not run the unit.
- A bare `qvm-features sys-foo <name> 1` (no `service.` prefix) does **not**
  create that file. This is a common silent failure.
- Remove with `qvm-features --unset` / `qvm-service --unset`. Upstream also
  uses `qvm-features <qube> appmenus-dispvm ''`.

## 6. Named disposables as service qubes

From `disposable-customization.rst`. Only for **stateless** service qubes
(or ones whose state you deliberately put in the dvm template, per section 2).

```bash
# no PCI devices (sys-firewall-like, VPN/mesh gateways)
qvm-create --class DispVM --template dvm-foo --label green sys-foo   # or: qvm-create --disp ...
qvm-prefs sys-foo autostart true
qvm-prefs sys-foo netvm <upstream-netvm>
qvm-prefs sys-foo provides_network true
qvm-features sys-foo appmenus-dispvm ''
```

With PCI devices (sys-net/sys-usb-like), additionally: `virt_mode hvm`,
`maxmem 0`, `netvm ''`, and `qvm-pci attach --persistent sys-foo dom0:<BDF>`
(USB controllers often need `-o no-strict-reset=True`).

When it replaces an existing service qube, set the old one's
`autostart false` and repoint every reference: other qubes' `netvm`,
`qubes-prefs default_netvm` / `updatevm` / `clockvm`, and qrexec policies.

`--label` is mandatory for `qvm-create`. Disposables inherit `netvm` and
firewall settings from their dvm template unless overridden on the
disposable.

## 7. Firewalling inside a disposable (Qubes 4.2+ is nftables)

- Qubes owns `table ip qubes` / `table ip6 qubes`. The `input` base chain has
  **policy drop** and jumps to `custom-input` first. `forward` jumps to
  `custom-forward`. Put your rules in the `custom-*` chains and re-add them
  every boot, because the tables are rebuilt at start.
- `nft insert` **prepends** and `nft add` **appends**. Inserting an accept
  and then a drop leaves the drop on top. Prefer `add` in the order you mean.
- **Every base chain on a hook is evaluated. A drop in any of them is final;
  an accept only ends its own chain.** Effective policy is the intersection.
- Third-party daemons may inject rules into Qubes' chains. NetBird, for
  example, prepends `iifname "wt0" accept` to every foreign input/forward
  base chain, which skips `custom-input` for that interface, and re-adds it
  if removed. A guard that must hold goes in **your own table on a hook the
  daemon doesn't touch** (e.g. a `prerouting` filter chain). Always check
  the result with `nft list ruleset` on the running qube.
- ufw/iptables-nft does not replace Qubes' nftables: it adds a parallel
  `filter` table, which is subject to the same injection. Use nft directly.

## 8. dom0 provisioning script patterns

- **Idempotent:** check before create (`qvm-ls --raw-list | grep -qxF`), use
  `qvm-start --skip-if-running`, guard `qvm-shutdown --wait` with
  `qvm-check --quiet --running`. Re-running must converge, not fail.
- **Cycle explicitly:** shut down the TemplateVM after root changes and the
  dvm template after `/rw` changes, *before* starting the disposable. Shut
  down disposable and dvm template at the top of the script.
- **Push code in, never pull data out:** `qvm-run --pass-io -u root <qube> --
  bash -s <<'EOF' ... EOF`. Quote the heredoc delimiter unless you mean to
  interpolate, and escape `\$` when you do. Never copy files from a domU
  into dom0: dom0 must not parse data from a qube.
- **Secrets:** take them from env or a file in dom0, send them through stdin,
  `set +x`, never echo them, never hard-code them. Don't store them in a
  shared dvm template unless every disposable from it should hold them.
- **Templates need a netvm to install packages.** Clones of a TemplateVM
  stay TemplateVMs (`qvm-clone` keeps the class). Install non-default
  packages in a dedicated clone, not the shared base template.
- **Verify the real thing:** finish by restarting the disposable from dom0
  and asserting the persisted state is live (daemon logged in, rules present
  in the expected order) inside the fresh boot.

## 9. Anti-patterns

- Configuring, enrolling or installing inside the disposable and expecting
  it to survive.
- Writing to a running dvm template, then starting the disposable without
  shutting the dvm template down.
- Installing packages in the dvm template (an AppVM): its root is discarded.
- Using a `default-dvm`-style shared dvm template for a qube holding secrets.
- Assuming `rc.local` runs before the network (it doesn't), or that a rule in
  `custom-input` is final (other base chains still apply, and daemons may
  insert above it).
- Setting a feature without the `service.` prefix and expecting a service
  flag.

## 10. Checklist for a new disposable service qube

- [ ] TemplateVM clone holds packages, units, drop-ins. Shut down after.
- [ ] Dvm template: `template_for_dispvms True`, no `appmenus-dispvm`, bind-dirs
      and hooks in `/rw/config`, executable. Shut down after.
- [ ] Stateful login done in the dvm template, then it's shut down.
- [ ] Named disposable: label, `netvm`, `provides_network` if it routes,
      `autostart` if it's infrastructure, `appmenus-dispvm ''`.
- [ ] Service flags via `qvm-service`, per-instance values via `vm-config.*`.
- [ ] Firewall rules checked with `nft list ruleset` after a fresh boot.
- [ ] Old qube's references repointed and its autostart disabled.
