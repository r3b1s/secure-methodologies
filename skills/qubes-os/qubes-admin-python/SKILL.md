---
name: qubes-admin-python
description: Writing Python against qubesadmin, the Qubes OS library that wraps the Admin API (the same library the qvm-* tools are built on) — for provisioning scripts, declarative config management and reconcilers, event watchers, and automation run from dom0 or from a management qube. Covers how it reaches qubesd (local socket in dom0, policy-checked qrexec elsewhere), the object model (domains, properties, features, services, tags, firewall, devices, volumes, disposables), value types and idempotent read-compare-write, errors and the traps that hide policy denials, call counts and caching, events, offline testing with QubesTest, and the qrexec policy a management qube needs. Use when writing or reviewing Python that imports qubesadmin, replacing qvm-* shell scripts with Python, or working out which Admin API calls code makes and how to scope them. For the qvm-* command-line tools use qubes-dom0-cli instead.
license: MIT
metadata:
  verified-on: "qubes-core-admin-client 4.3.35 and qubes-core-admin 4.3.53 (Qubes OS R4.3) source; examples tested offline with QubesTest"
---

# qubesadmin: the Python library over the Qubes Admin API

`qubesadmin` is a Python library that wraps the Qubes OS **Admin API**,
the `admin.*` qrexec services served by `qubesd` in dom0. Every `qvm-*`
tool is a thin command-line layer over it. Upstream ships it in
`qubes-core-admin-client`, but in code it is just a library: it turns
method calls into Admin API calls and reply bytes into Python objects.

What was checked, and how: the library source (`qubes-core-admin-client`
4.3.35, branch `r43`) and the server it talks to (`qubes-core-admin`
4.3.53), read in 2026-10. The example in `assets/` is tested against the
library's own `QubesTest` fake. Nothing here was run on a live R4.3.2
system. Sources of truth:

- Library: https://github.com/QubesOS/qubes-core-admin-client
  (`qubesadmin/`; the `qubesadmin/tools/qvm_*.py` files are the best usage
  examples for any operation)
- Server and API: https://github.com/QubesOS/qubes-core-admin
  (`qubes/api/admin.py`) and `developer/services/admin-api.rst` in
  https://github.com/QubesOS/qubes-doc
- Policy engine: https://github.com/QubesOS/qubes-core-qrexec

When the installed library disagrees with this file, the library wins.
Read it in place: `python3 -c 'import qubesadmin; print(qubesadmin.__file__)'`.

## 1. Where the code runs decides what it may do

```python
import qubesadmin
app = qubesadmin.Qubes()
```

`Qubes()` checks for `/etc/qubes-release` (present only in dom0) and
returns one of two transports:

| | `QubesLocal` (dom0) | `QubesRemote` (any other qube) |
|---|---|---|
| How a call travels | written straight to `/var/run/qubesd.sock` | one `qrexec-client-vm <dest> admin.X+arg` process **per call** |
| Caller as `qubesd` sees it | `dom0` (the library writes the header itself) | the calling qube |
| qrexec policy | **not consulted: full control** | checked on every call |
| Running as another user (`user=`) | allowed | raises `ValueError` |

The same script is all-powerful in dom0 and exactly as powerful as
policy allows anywhere else. Develop and test against a management qube
whenever possible: denials there show you what the code really touches.

Install in a management qube's template: `python3-qubesadmin` (library
only) or `qubes-core-admin-client` (library and `qvm-*` tools), from the
Qubes repository of the **same release as dom0**, not from pip. The
library and `qubesd` change together (see §11).

## 2. Object model

```python
app.domains                      # dict-like collection of QubesVM
vm = app.domains["work"]         # KeyError if absent (lists all qubes first)
vm.name, vm.klass                # "AppVM", "TemplateVM", "DispVM", ...
vm.netvm                         # property: read = Get, assign = Set, del = Reset
vm.property_is_default("netvm")  # True if following the default
app.default_netvm                # global properties live on app
vm.features["vm-config.x"]       # dict-like, values are str
vm.features.check_with_template("os")
vm.tags                          # set-like: in / add / discard / remove
vm.firewall.rules                # list of qubesadmin.firewall.Rule
vm.devices["pci"]                # DeviceCollection (4.3 devices API)
vm.volumes["private"]            # Volume: size, resize(), revisions, ...
vm.get_power_state()             # "Running", "Halted", ... ("NA" if denied)
app.labels["red"], app.pools["default"]
```

Every attribute access is a call. [references/api-map.md](references/api-map.md)
maps each operation to the exact Admin API call and argument.

## 3. Values: types, defaults and comparisons

A property read returns a typed value: `vm`-typed → a `QubesVM` (or
`None`), `label` → a `Label`, `bool`, `int`, `str`. An unset `int`/`bool`
raises `AttributeError`.

```python
vm.netvm = "sys-firewall"        # a name or a QubesVM both work
vm.netvm = None                  # sends "": no network
del vm.netvm                     # reset to the default (same as = qubesadmin.DEFAULT)
vm.memory = 800                  # sent as "800"
vm.include_in_backups = True     # sent as "True"
```

- **Compare as strings.** `str()` of a `QubesVM`/`Label` is its name, and
  `None` should compare as `""`. Comparing a `QubesVM` with a string, or
  `1` with `"1"`, reports false drift.
- **"Equal to the default" is not "set".** If `property_is_default()` is
  true, the qube follows the global default and will change when it
  does. Decide whether your code pins values or follows defaults.
- **Features are always strings.** `vm.features[k] = True` stores `"1"`,
  `False` stores `""` (present but false), and `del vm.features[k]`
  removes it (back to the template's or the default behaviour).
  `vm.features.get(k)` returns `None` when absent.
- **Services are features:** `service.<name>` = `"1"` (on), `""` (off),
  absent (template default). That is all `qvm-service` does.
- `vm.tags` has no "set exactly these" operation. Adding is `tags.add`;
  removing someone else's tags (`created-by-*`) is refused.

## 4. Lifecycle

```python
vm = app.add_new_vm("AppVM", "dev", "purple", template="fedora-44-xfce")
tpl = app.add_new_vm("TemplateVM", "tpl-x", "black")          # no template
vm = app.add_new_vm("AppVM", "big", "red", template="t", pools={"private": "vm-pool"})
new = app.clone_vm("fedora-44-xfce", "tpl-dev")               # keeps the class
del app.domains["old"]                                        # admin.vm.Remove
vm.start()                       # no-op if already running
vm.shutdown(wait=True)           # waits server-side
vm.kill()
```

- `add_new_vm` is one call; the new qube is tagged
  `created-by-<caller>` by `qubesd`.
- **`clone_vm` is not one call.** It creates the qube and then copies, call
  by call, every non-default property, tag, feature, firewall rule and
  device assignment, then the volumes (`CloneFrom`/`CloneTo`). It also runs
  the dom0 tool `qvm-appmenus` locally. If any step fails the library
  **deletes the new qube** and re-raises, unless `ignore_errors=True`,
  which turns failures into log lines. In a management qube without
  `qvm-appmenus` you need `ignore_errors=True`, and then must check the
  result yourself.
- Changing `template` needs the qube halted (`QubesVMNotHaltedError`). Some
  properties only take effect at the next start.
- Removing a qube that others reference (`template`, `netvm`,
  `default_dispvm`) fails; repoint them first.

## 5. Running things inside qubes

These are qrexec **services**, not Admin API calls, and need their own
policy lines.

```python
out, err = vm.run("ls -l /rw")                       # qubes.VMShell (shell string)
out, err = vm.run_with_args("ls", "-l", path)        # qubes.VMExec: no shell parsing
out, err = vm.run("dnf -y update", user="root")      # qubes.VMRootShell when supported
p = vm.run_service("my.Service+arg")                 # any service -> subprocess.Popen
out, err = vm.run_service_for_stdio("qubes.GetDate") # raises CalledProcessError on rc != 0
```

- Prefer `run_with_args` for anything containing data you didn't write:
  it avoids the shell. It falls back to quoting when the target lacks the
  `vmexec` feature.
- From a qube, `user="root"` works only through `qubes.VMRootShell`
  (targets that advertise `supported-rpc.qubes.VMRootExec`). Otherwise it
  raises `ValueError`.
- Disposables: `qubesadmin.vm.DispVM.from_appvm(app, "default-dvm")`
  returns a wrapper whose first `run_service*` creates the disposable. From
  a qube the call goes to `@dispvm:default-dvm` and cleans itself up. In
  dom0 the library calls `admin.vm.CreateDisposable` and you must call
  `.cleanup()` afterwards.

## 6. Errors

`qubesd` returns an exception's class name; the library re-raises the
class of the same name from `qubesadmin.exc`. Useful ones:
`QubesVMNotFoundError`, `QubesVMNotHaltedError`,
`QubesVMNotRunningError`, `QubesNoSuchPropertyError`,
`QubesPropertyValueError`, `QubesValueError`, `QubesMemoryError`,
`QubesFeatureNotFoundError`, `QubesTagNotFoundError`,
`DeviceAlreadyAssigned`, `DeviceNotAssigned`, `BackupAlreadyRunningError`.
All derive from `QubesException`, except `PermissionDenied` (and
`ProtocolError`).

Policy denials, which are easy to miss:

- A refused call (qrexec policy, or `qubesd` itself) arrives as
  `QubesDaemonAccessError`. The reason is only in dom0's journal.
- A refused **property** read becomes `QubesPropertyAccessError`, which
  is also an `AttributeError`. So `hasattr(vm, "netvm")` and
  `getattr(vm, "netvm", None)` silently turn "denied" into "unset". Catch
  it explicitly:

  ```python
  try:
      value = getattr(vm, key)
  except qubesadmin.exc.QubesPropertyAccessError:
      raise                           # denied: a policy problem, not "unset"
  except AttributeError:
      value = None                    # genuinely has no value
  ```

- `get_power_state()` returns `"NA"` when denied, so `is_running()` is
  `False`.
- Several `KeyError` subclasses (`QubesVMNotFoundError`,
  `QubesFeatureNotFoundError`, ...) mean `dict.get`-style code treats
  them as "absent". That is right for features, wrong if you expected an
  error.

## 7. Call counts, caching and lookups

From a qube each call is a process launch plus a qrexec round trip, so
call count is the cost.

- `app.domains[name]`, `name in app.domains` and iterating all call
  `admin.vm.List` once per collection (cached until a create, remove or
  event clears it). `app.domains.get_blind(name)` or
  `app.blind_mode = True` skips the existence check. Use these when
  policy lets the code see only a few qubes.
- `property_is_default(p)` and reading `p` are **two** `Get` calls.
- `app.cache_enabled = True` makes the first read on each qube fetch all
  properties at once (`GetAll`), served from cache afterwards. Nothing
  refreshes that cache except `EventsDispatcher`, and your own `Set`
  calls do not update it. Use it only in short read-then-write runs, or
  together with a running dispatcher. The stock policy denies `GetAll`,
  and the library then quietly falls back to per-property calls (see
  [references/policy.md](references/policy.md)).
- `list(vm.features)` / `.items()` is one `List` plus one `Get` per
  feature. Ask for the keys you care about instead.

## 8. Events

```python
import asyncio
from qubesadmin.events import EventsDispatcher

def on_event(subject, event, **kwargs):     # subject: QubesVM or None; kwargs are str
    print(subject, event, kwargs)

d = EventsDispatcher(app)                   # admin.Events; turns app.cache_enabled on
d.add_handler("domain-start", on_event)
d.add_handler("property-set:netvm", on_event)
d.add_handler("*", on_event)                # everything: handy to discover event names
asyncio.run(d.listen_for_events())          # never returns; reconnects on its own
```

- Creating a dispatcher enables the property cache. If you never run
  `listen_for_events()`, that cache goes stale: pass `enable_cache=False`
  if you only construct one.
- The stream is filtered by policy: from a qube you see events only for
  qubes your rules allow, plus system events if `admin.Events` to `dom0`
  is allowed.
- `EventsDispatcher(app, api_method="admin.vm.Stats")` streams
  `vm-stats` events instead.
- On reconnect the dispatcher emits `connection-established` and drops
  all caches. Treat it as "state may have changed while I was away".

## 9. Writing configuration management with it

The library makes no attempt at idempotency. The pattern that works:

1. **Desired state is data** (JSON/YAML/dict), not code: qubes, their
   class, template, label, properties, features, services, tags.
2. **Order by dependency:** templates before the qubes based on them,
   netvms before their clients.
3. **Read, compare, write only on difference.** Compare as strings
   (§3), treat "default" as its own state, and make removal explicit
   (`null` means remove a feature; never delete unlisted things).
4. **Dry run by default.** Print a plan with old → new values; change
   things only with `--apply`.
5. **Don't force disruptive steps.** A template change on a running qube
   is reported as blocked rather than shutting the qube down.
6. **Carry on past a failed step, and report it.** Exit non-zero if
   anything failed or was blocked.
7. **Run it from a management qube** with explicit policy for exactly
   the calls it makes, scoped to `@tag:created-by-<mgmt>` (see
   [references/policy.md](references/policy.md)). Keep a dom0 run as the
   fallback for bootstrapping.

[assets/reconcile.py](assets/reconcile.py) implements this for qubes,
properties, features, services and tags, with
[assets/test_reconcile.py](assets/test_reconcile.py) as offline tests.
Copy and extend them. Firewall rules (`vm.firewall.rules = [...]`) and
device assignments (`vm.devices[c].assign(...)`) follow the same
pattern. Compare `str(rule)` lists, and assignments by device and mode.

## 10. Testing without a Qubes system

`qubesadmin.tests.QubesTest` is a fake app. You script the replies to
the Admin API calls you expect; any other call raises `AssertionError`;
every call is recorded.

```python
from qubesadmin.tests import QubesTest

app = QubesTest()
app.expected_calls[("dom0", "admin.vm.List", None, None)] = \
    b"0\x00work class=AppVM state=Halted uuid=0\n"
app.expected_calls[("work", "admin.vm.property.Get", "netvm", None)] = \
    b"0\x00default=True type=vm sys-firewall"
app.expected_calls[("work", "admin.vm.property.Set", "netvm", b"sys-netbird")] = b"0\x00"

ensure_netvm(app, "work", "sys-netbird")          # your code, given app
assert ("work", "admin.vm.property.Set", "netvm", b"sys-netbird") in app.actual_calls
```

- Keys are `(dest, method, arg, payload)`; `arg` and `payload` are `None`
  when absent, and a payload is `bytes`.
- A reply is `b"0\x00" + body` for success. An exception reply is
  `b"2\x00<ExceptionClass>\x00\x00<message>\x00"`. `b""` simulates a
  refused call. A list of replies is consumed one per call.
- Common bodies: `admin.vm.List` → `name class=… state=… uuid=…\n` per
  qube; `property.Get` → `default=<True|False> type=<str|int|bool|vm|label> <value>`;
  `feature.Get` → the value; `tag.Get` → `1`/`0`;
  `CurrentState` → `power_state=Running mem=…`.
- `app.actual_calls` after a run **is** your policy footprint: every
  `(dest, method, arg)` in it needs an allow rule when the code runs
  from a qube.
- Write code that takes `app` as a parameter, so tests can pass a
  `QubesTest`. `qubesadmin.tests.mock_app` builds richer fake systems.

Run tests with `python3-qubesadmin` installed, or with a
`qubes-core-admin-client` checkout on `sys.path`. No Qubes system is
needed.

## 11. Raw calls and version drift

- **Escape hatch:** `app.qubesd_call(dest, method, arg=None, payload=None)`
  sends any Admin API call through the active transport and returns the
  reply body as bytes (errors raised as above). Use it for calls the
  library does not wrap (`admin.label.Create`,
  `admin.vm.feature.CheckWithNetvm`, ...).
- **Not in this library:** the policy-editing API (`policy.*`) lives in
  `qubes-core-qrexec` (`qrexec.policy.admin_client.PolicyClient`, CLI
  `qubes-policy`).
- **The Python API is not promised stable across releases.** R4.3
  replaced the device API: R4.2's `assignments()`, `persistent()`,
  `update_persistent()` and `DeviceAssignment(backend, ident, persistent=)`
  became `get_assigned_devices()`, `assign()`/`unassign()`,
  `update_assignment(device, AssignmentMode)` and
  `DeviceAssignment.new(backend, port_id, devclass, device_id, mode=)`.
  PCI assignments must use mode `"required"`. Keep the library at dom0's
  release, and re-run your tests after a major upgrade.

## 12. Gotchas

- **dom0 bypasses policy.** Code that "works in dom0" proves nothing
  about what it will need in a management qube.
- **`@anyvm` never matches dom0** in policy: listing all qubes, all
  events, global properties and creating qubes need a `dom0` rule.
- **Denials look like "unset"** through `getattr`/`hasattr` (§6), and like
  "halted" through `is_running()`.
- **`clone_vm` deletes its half-made clone on error** and needs
  `qvm-appmenus` (§4).
- **Feature `False` is not feature absent** (`""` vs removed).
- **Stale caches:** `cache_enabled` without a running dispatcher.
- **Names come from qubesd.** Treat qube names, feature values and
  event kwargs as data: they reach your code from whatever qubes
  are allowed to set them. Pass them as arguments (`run_with_args`), never
  into a shell string or a policy file unchecked.

References in this skill:
[references/api-map.md](references/api-map.md) (operation → Admin API
call → policy argument),
[references/policy.md](references/policy.md) (scoping a management
qube, and the grants that make it equal to dom0).

Companion skills from the same collection, installed separately:
`qubes-dom0-cli` (the `qvm-*` tools and policy files in dom0),
`qubes-vm-cli` (tools inside qubes) and `qubes-disposable-vms`
(disposable patterns and dom0 provisioning scripts).
