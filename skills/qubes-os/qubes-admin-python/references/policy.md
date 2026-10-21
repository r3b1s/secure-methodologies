# qrexec policy for qubesadmin code in a management qube

In dom0, qubesadmin talks to `qubesd` over its local socket and **no policy
applies**. Everywhere else every call goes through qrexec policy in dom0.
This page is about the second case. Read from `qubes-core-admin` 4.3.53,
`qubes-core-qrexec` and `qubes-core-admin-client` 4.3.35.

## Rule shape

```text
# service              argument   source  destination           action
admin.vm.property.Set  +netvm     mgmt    @tag:created-by-mgmt  allow target=dom0
```

- Put rules in dom0 at `/etc/qubes/policy.d/30-<name>.policy`. Files are
  read in name order and the first matching rule wins. Stock admin
  defaults are in `90-admin-default.policy` (do not edit it), and the
  first rule that matches anywhere wins.
- **Every `admin.*` allow/ask rule needs `target=dom0`.** Without it qrexec
  routes the call to the destination qube, which starts that qube and then
  fails anyway.
- **`@anyvm` never matches dom0.** Calls whose destination *is* dom0 need
  a `dom0` (or `@adminvm`) rule: `admin.vm.List` when listing everything,
  `admin.Events` for all qubes, every `admin.property.*` (global) call,
  `admin.vm.Create.*`, and `admin.label.*` / `admin.pool.*`.
- For `admin.vm.List` and `admin.Events` sent to dom0, `qubesd` then
  re-checks the same call against each qube and drops the ones this source
  may not see. You need **both** the `dom0` rule and a per-qube rule.
- The argument column is `*` or one exact `+value`. There are no prefixes
  or wildcards inside an argument.
- Policy never sees payloads, so it cannot restrict a value: "may set
  `netvm`" cannot become "may set `netvm` only to `sys-firewall`".
  `qubesd` adds no value checks of its own either. A script that looks up
  the qube it is about to name (`app.domains['sys-firewall']`) needs that
  qube to be visible to `admin.vm.List`; setting `vm.netvm =
  'sys-firewall'` as a string does not.

## How denials show up in code

| Where it was refused | What the caller sees | What qubesadmin raises |
|---|---|---|
| qrexec policy (no matching allow) | `qrexec-client-vm` exits 126 | `QubesDaemonAccessError` |
| inside `qubesd` (e.g. the List filter, a protected tag) | empty reply | `QubesDaemonAccessError` ("See journalctl in dom0") |
| a property read or write | either of the above | `QubesPropertyAccessError`, which is **also an `AttributeError`**: `hasattr()` and `getattr(vm, p, default)` hide it |
| `get_power_state()` | either | no exception: returns `'NA'` |
| the `GetAll` cache prefill | either | no exception: falls back to one `Get` per property |

dom0's journal logs every refusal (`journalctl -u qubesd`, and the qrexec
policy daemon's log).

## Scope the qube to what it created

`qubesd` tags every qube created through the API with
`created-by-<caller>` (and API-made disposables also with
`disp-created-by-<caller>`). Only dom0 can add or remove a `created-by-*`
tag, so it is a sound selector. `managed-by-*` and other tags are
conventions: anything allowed `admin.vm.tag.Set` on a qube can add them.

### Explicit rules (recommended for scripts)

List exactly the calls the code makes: the [api-map.md](api-map.md)
table, or a `QubesTest` run's `actual_calls` (see SKILL.md). This is
the policy for `assets/reconcile.py` run from a qube named `mgmt`:

```text
# --- reading ---------------------------------------------------------------
admin.vm.List          *  mgmt  dom0                  allow target=dom0
admin.vm.List          *  mgmt  @tag:created-by-mgmt  allow target=dom0
admin.vm.property.Get  *  mgmt  @tag:created-by-mgmt  allow target=dom0
admin.vm.feature.Get   *  mgmt  @tag:created-by-mgmt  allow target=dom0
admin.vm.tag.Get       *  mgmt  @tag:created-by-mgmt  allow target=dom0
admin.vm.CurrentState  *  mgmt  @tag:created-by-mgmt  allow target=dom0

# --- creating: pin the templates it may build on --------------------------
admin.vm.Create.AppVM  +fedora-44-xfce  mgmt  dom0    allow target=dom0

# --- writing: per property / feature, only on its own qubes ---------------
admin.vm.property.Set    +netvm     mgmt  @tag:created-by-mgmt  allow target=dom0
admin.vm.property.Set    +memory    mgmt  @tag:created-by-mgmt  allow target=dom0
admin.vm.property.Set    +label     mgmt  @tag:created-by-mgmt  allow target=dom0
admin.vm.property.Reset  *          mgmt  @tag:created-by-mgmt  allow target=dom0
admin.vm.feature.Set     *          mgmt  @tag:created-by-mgmt  allow target=dom0
admin.vm.feature.Remove  *          mgmt  @tag:created-by-mgmt  allow target=dom0
admin.vm.tag.Set         +managed-by-mgmt  mgmt  @tag:created-by-mgmt  allow target=dom0
```

Cloning (`app.clone_vm`) needs far more: read access on the source
(property, feature and tag lists, firewall, devices, volumes), the
matching writes on the new qube, and `admin.vm.volume.CloneFrom` on the
source plus `CloneTo` on the copy. Run it once against `QubesTest`, or
watch the dom0 journal, to collect the list.

### The stock include files (coarse)

`90-admin-default.policy` sends every call to one of four include files,
all empty by default:

| Include | Covers |
|---|---|
| `include/admin-local-ro` | per-qube reads (also includes `admin-local-rwx`) |
| `include/admin-local-rwx` | per-qube writes and actions, **including `admin.vm.Console` and `admin.vm.volume.Import`/`ImportWithSize`** |
| `include/admin-global-ro` | global reads, listing (also includes `admin-global-rwx`) |
| `include/admin-global-rwx` | global writes, **including `admin.vm.Create.*` and `admin.property.Set`** |

Lines in an include file have no service or argument column:

```text
# include/admin-local-rwx
mgmt  @tag:created-by-mgmt  allow target=dom0
# include/admin-global-ro
mgmt  @adminvm              allow target=dom0
mgmt  @tag:created-by-mgmt  allow target=dom0
```

This is what the qubes-ansible "management VM" setup uses. It is quick,
but local-rwx is shell-level access (Console, root-volume import) to
every qube it covers. Never put the management qube itself, templates
used by other qubes, or `@anyvm` in a `-rwx` include.

## Grants that make a management qube equal to dom0

However narrowly the rest is written:

- `policy.Replace` / `policy.include.Replace` (the stock policy says so).
- `admin.property.Set` on `management_dispvm`, `updatevm`,
  `default_template`, `default_netvm`, `default_dispvm`, `default_guivm`.
- `qubes.VMShell` / `VMRootShell` / `VMExec`, `admin.vm.volume.Import*`,
  or `admin.vm.Console` on a **template** (or any qube it doesn't own).
- Write access to **itself**: with `admin.vm.feature.Set` on itself it can
  set `tag-created-vm-with`, and every qube it then creates carries any
  tag it likes, reaching every `@tag:` rule in the policy.
- `admin.vm.device.pci.*` and block devices from dom0-backed backends. Pin
  the device argument (`+<backend>+<port>+<id>`) if you grant these.

## GetAll and the cache

`91-admin-default-deny.policy` denies `admin.vm.property.GetAll` and
`admin.property.GetAll` (with `notify=no`). With `app.cache_enabled =
True` the library then quietly does one `Get` per property. To get the
one-call prefill, allow it in your lower-numbered file:

```text
admin.vm.property.GetAll  *  mgmt  @tag:created-by-mgmt  allow target=dom0
```

`GetAll` returns every property, so only allow it where `Get *` is
already allowed.
