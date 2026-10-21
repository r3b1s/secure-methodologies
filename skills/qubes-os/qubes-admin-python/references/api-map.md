# qubesadmin → Admin API call map

Which Admin API call each library operation sends: what a qrexec policy
line has to match when the code runs outside dom0. Read from
`qubes-core-admin-client` 4.3.35 (branch `r43`).

Columns: **call** is the qrexec service name. **dest** is the destination
the policy rule must match (every `admin.*` rule also needs `target=dom0`).
**arg** is the argument after `+`, which a rule can pin exactly or match
with `*`.

## Collections and lookup

| Library | Call | dest | arg |
|---|---|---|---|
| `for vm in app.domains`, `name in app.domains`, `app.domains[name]` | `admin.vm.List` | `dom0` (then filtered per qube) | — |
| `app.domains.get_blind(name)`, or with `app.blind_mode = True` | nothing until you use the object | | |
| `vm.klass` (when not known from the list) | `admin.vm.List` | vm | — |
| `del app.domains[name]` | `admin.vm.Remove` | vm | — |
| `app.labels`, `app.get_label()` | `admin.label.List` / `Get` / `Index` | `dom0` | label |
| `app.pools`, `app.pool_drivers` | `admin.pool.List` / `ListDrivers` / `Info` | `dom0` | pool |

The list is fetched once per `VMCollection` and kept until something
calls `clear_cache()` (create, remove, or an event).

## Properties

| Library | Call | dest | arg |
|---|---|---|---|
| `vm.prop` (read), `vm.property_is_default(prop)` | `admin.vm.property.Get` | vm | prop |
| `vm.prop = value` | `admin.vm.property.Set` (payload: value) | vm | prop |
| `del vm.prop`, `vm.prop = qubesadmin.DEFAULT` | `admin.vm.property.Reset` | vm | prop |
| `vm.property_get_default(prop)` | `admin.vm.property.GetDefault` | vm | prop |
| `vm.property_list()` | `admin.vm.property.List` | vm | — |
| first read with `app.cache_enabled = True` | `admin.vm.property.GetAll` | vm | — |
| the same on `app` (global properties) | `admin.property.*` | `dom0` | prop |

`property_is_default()` and reading the value are two separate `Get`
calls unless caching is on. A denied `GetAll` is silently ignored, and
the library falls back to one `Get` per property.

## Features, tags, notes

| Library | Call | dest | arg |
|---|---|---|---|
| `vm.features[k]`, `vm.features.get(k)` | `admin.vm.feature.Get` | vm | k |
| `vm.features[k] = v` | `admin.vm.feature.Set` (payload: `str(v)`; `True`→`1`, `False`→empty) | vm | k |
| `del vm.features[k]` | `admin.vm.feature.Remove` | vm | k |
| `list(vm.features)`, `vm.features.items()` | `admin.vm.feature.List`, then one `Get` per feature | vm | — / k |
| `vm.features.check_with_template(k)` | `admin.vm.feature.CheckWithTemplate` | vm | k |
| `t in vm.tags` | `admin.vm.tag.Get` | vm | t |
| `vm.tags.add(t)` | `admin.vm.tag.Set` | vm | t |
| `vm.tags.remove(t)` / `discard(t)` | `admin.vm.tag.Remove` | vm | t |
| `list(vm.tags)` | `admin.vm.tag.List` | vm | — |
| `vm.get_notes()` / `vm.set_notes(s)` | `admin.vm.notes.Get` / `Set` | vm | — |

Services are features: `qvm-service` stores `service.<name>` (`1` = on,
empty = off, absent = template default).

## Lifecycle and state

| Library | Call | dest | arg |
|---|---|---|---|
| `app.add_new_vm(cls, name, label, template=)` | `admin.vm.Create.<cls>` (payload `name=… label=…`) | `dom0` | template |
| … with `pool=` or `pools=` | `admin.vm.CreateInPool.<cls>` | `dom0` | template |
| `app.clone_vm(src, name, …)` | **many**: Create, then Get/Set for every non-default property, tag, feature and firewall rule, device assignments, `admin.vm.volume.CloneFrom` on the source plus `CloneTo` on the copy, and a local `qvm-appmenus` run | | |
| `vm.start()` | `admin.vm.Start` | vm | — |
| `vm.shutdown(force=, wait=)` | `admin.vm.Shutdown` | vm | none, `force`, `wait` or `force+wait` |
| `vm.kill()` | `admin.vm.Kill` | vm | — |
| `vm.pause()` / `unpause()` | `admin.vm.Pause` / `Unpause` | vm | — |
| `vm.suspend()` / `resume()` | `admin.vm.Suspend` / `Resume` (no qrexec service is installed for these in 4.3: dom0 only) | vm | — |
| `vm.get_power_state()`, `is_running()`, `is_halted()`, `get_mem()` | `admin.vm.CurrentState` | vm | — |

`get_power_state()` returns `'NA'` when the call is denied, so
`is_running()` is then `False` rather than an error.

## Running things inside qubes (qrexec services, not Admin API)

| Library | Service | Notes |
|---|---|---|
| `vm.run(cmd)` | `qubes.VMShell` | shell string |
| `vm.run(cmd, user='root')` | `qubes.VMRootShell` if the qube advertises `supported-rpc.qubes.VMRootExec`; otherwise `qubes.VMShell` with `user=root`, which works only in dom0 (from a qube, `user=` raises `ValueError`) | |
| `vm.run_with_args(*argv)` | `qubes.VMExec+<encoded argv>` (`qubes.VMRootExec+…` for root) | falls back to quoting into `qubes.VMShell` when the `vmexec` feature is missing |
| `vm.run_service(name)`, `app.run_service(dest, name)` | `name` | any service |
| `DispVM.from_appvm(app, dvm).run_service(name)` | in a qube: `name` to `@dispvm:<dvm>`; in dom0: `admin.vm.CreateDisposable` first | in dom0 call `.cleanup()` afterwards |

These need their own policy lines, which are not `admin.*` lines, and
take no `target=dom0`. `qubes.VMShell` / `VMRootShell` / `VMExec` into a
template is code execution in every qube based on it.

## Firewall, devices, storage, backups, events

| Library | Call | dest | arg |
|---|---|---|---|
| `vm.firewall.rules` (first read) | `admin.vm.firewall.Get` | vm | — |
| `vm.firewall.rules = [...]`, `save_rules()` | `admin.vm.firewall.Set` (payload: all rules) | vm | — |
| `vm.firewall.reload()` | `admin.vm.firewall.Reload` | vm | — |
| `vm.devices[c].get_assigned_devices()` | `admin.vm.device.<c>.Assigned` | vm | — |
| `vm.devices[c].get_attached_devices()` | `admin.vm.device.<c>.Attached` | vm | — |
| `backend.devices[c].get_exposed_devices()` | `admin.vm.device.<c>.Available` | backend | — |
| `vm.devices[c].assign(a)` / `unassign(a)` | `admin.vm.device.<c>.Assign` / `Unassign` | vm | `<backend>+<port>+<device id>` |
| `vm.devices[c].attach(a)` / `detach(a)` | `admin.vm.device.<c>.Attach` / `Detach` | vm | same |
| `vm.devices[c].update_assignment(dev, AssignmentMode.…)` | `admin.vm.device.<c>.Set.assignment` (payload: mode) | vm | same |
| `vm.devices.deny(*ifaces)` / `allow(...)` | `admin.vm.device.denied.Add` / `Remove` | vm | — |
| `vm.volumes` | `admin.vm.volume.List` | vm | — |
| `vol.size`, `vol.pool`, … | `admin.vm.volume.Info` | vm | volume |
| `vol.resize(n)` / `revert(r)` / `clear_data()` | `admin.vm.volume.Resize` / `Revert` / `Clear` | vm | volume |
| `vol.revisions` | `admin.vm.volume.ListSnapshots` | vm | volume |
| `vol.rw = …` / `ephemeral` / `revisions_to_keep` | `admin.vm.volume.Set.rw` / `Set.ephemeral` / `Set.revisions_to_keep` | vm | volume |
| `vol.import_data(f)` / `import_data_with_size(f, n)` | `admin.vm.volume.Import` / `ImportWithSize` | vm | volume |
| `dst.clone(src)` | `CloneFrom` on src, `CloneTo` on dst | each | volume |
| `EventsDispatcher(app)` | `admin.Events` | `dom0` (all) or vm | — |
| `EventsDispatcher(app, api_method='admin.vm.Stats')` | `admin.vm.Stats` | `dom0` or vm | — |
| backups (`qvm-backup` tooling) | `admin.backup.Execute` / `Info` / `Cancel` | `dom0` | profile name |

In the device argument, unknown parts of a device id are written as `_`.
Use `*` unless the rule should cover exactly one device.

## Policy API (not in qubesadmin)

`policy.List/Get/Replace/Remove`, `policy.include.*` and
`policy.GetFiles` are served by qrexec itself. Their Python client is
`qrexec.policy.admin_client.PolicyClient` (package `qubes-core-qrexec`),
and the CLI is `qubes-policy`. The stock policy warns that write access
"effectively gives the caller full control over the system".
