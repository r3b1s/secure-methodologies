#!/usr/bin/python3
"""reconcile.py: bring qubes in line with a JSON description, using qubesadmin.

Runs in dom0, or in a management qube where qrexec policy decides what it may
touch. The default is a dry run that prints the plan; pass --apply to change
anything. Exit status: 0 if every step succeeded, 1 if any step failed or was
blocked.

Desired-state file:

    {
      "qubes": {
        "tpl-dev": {"class": "TemplateVM", "clone_from": "fedora-44-xfce",
                    "label": "black"},
        "dev": {
          "class": "AppVM", "template": "tpl-dev", "label": "purple",
          "prefs": {"netvm": "sys-firewall", "memory": 800,
                    "kernelopts": "@default"},
          "features": {"vm-config.example": "value", "old-feature": null},
          "services": {"crond": true, "cups": false},
          "tags": ["managed-by-mgmt"]
        }
      }
    }

Semantics:
- Missing qubes are created, or cloned when "clone_from" is set. Existing qubes
  are never removed.
- prefs: "@default" resets a property to its default. null means "no value"
  (netvm: null is offline). An explicit value is pinned even if it equals the
  current default, so it does not drift when the global default changes.
- features: null removes the feature; true/false are stored as "1"/"".
- services: shorthand for the features "service.<name>"; null removes.
- tags: listed tags are added; other tags are left alone.
- A template change on a running qube is reported as blocked, not forced.
"""
import argparse
import json
import shutil
import sys

import qubesadmin
import qubesadmin.exc

DEFAULT = "@default"
SPEC_KEYS = {"class", "label", "template", "clone_from", "prefs", "features",
             "services", "tags"}
# Properties that name another qube: used to order the work.
QUBE_PREFS = {"template", "netvm", "default_dispvm", "management_dispvm",
              "audiovm", "guivm"}
CLASS_ORDER = {"TemplateVM": 0, "StandaloneVM": 1, "AppVM": 2, "DispVM": 3}


def wire(value):
    """The string form qubesd uses for a property value.

    QubesVM and Label objects become their names, None becomes "", booleans
    become "True"/"False" (how qubesd reports them), ints become digits.
    """
    return "" if value is None else str(value)


def feature_wire(value):
    """The string qubesadmin stores for a feature value (see Features.__setitem__)."""
    if isinstance(value, bool):
        return "1" if value else ""
    return str(value)


def current_property(vm, key):
    """Read a property, telling "unset" apart from "not allowed to read".

    QubesPropertyAccessError subclasses AttributeError, so a plain
    getattr(vm, key, None) would turn a policy denial into "unset".
    """
    try:
        return getattr(vm, key)
    except qubesadmin.exc.QubesPropertyAccessError:
        raise
    except AttributeError:
        return None


def order(desired):
    """Qubes that others depend on (templates, netvms) come first."""
    deps = {}
    for name, spec in desired.items():
        refs = {spec.get("template"), spec.get("clone_from")}
        refs |= {v for k, v in spec.get("prefs", {}).items() if k in QUBE_PREFS}
        deps[name] = {r for r in refs if r in desired and r != name}
    done, result = set(), []
    while len(result) < len(desired):
        ready = sorted(
            (n for n in desired if n not in done and deps[n] <= done),
            key=lambda n: (CLASS_ORDER.get(desired[n].get("class"), 9), n))
        if not ready:
            raise ValueError("dependency cycle among: "
                             + ", ".join(sorted(set(desired) - done)))
        done.update(ready)
        result.extend(ready)
    return result


class Reconciler:
    def __init__(self, app, apply=False, out=print):
        self.app = app
        self.apply = apply
        self.out = out
        self.changes = 0
        self.failures = 0

    def step(self, qube, what, action):
        """Record one change; run it only when applying."""
        self.changes += 1
        self.out(f"{'apply' if self.apply else 'plan '}  {qube}: {what}")
        if not self.apply:
            return True
        try:
            action()
            return True
        except (qubesadmin.exc.QubesException,
                qubesadmin.exc.PermissionDenied) as err:
            self.fail(qube, what, err)
            return False

    def fail(self, qube, what, err):
        self.failures += 1
        hint = ""
        if isinstance(err, qubesadmin.exc.QubesDaemonAccessError):
            hint = " (denied by qrexec policy, or qubesd refused: see the dom0 journal)"
        self.out(f"FAILED {qube}: {what}: {type(err).__name__}: {err}{hint}")

    def run(self, desired):
        for name, spec in desired.items():
            unknown = set(spec) - SPEC_KEYS
            if unknown:
                raise ValueError(f"{name}: unknown keys {sorted(unknown)}")
        for name in order(desired):
            try:
                self.qube(name, desired[name])
            except (qubesadmin.exc.QubesException,
                    qubesadmin.exc.PermissionDenied) as err:
                self.fail(name, "reading current state", err)
        return self.changes, self.failures

    def qube(self, name, spec):
        if name not in self.app.domains:            # admin.vm.List (cached)
            if not self.create(name, spec):
                return
        vm = self.app.domains[name]

        want = dict(spec.get("prefs", {}))
        for key in ("label", "template"):
            if key in spec:
                want.setdefault(key, spec[key])
        for key, value in want.items():
            self.prop(vm, key, value)

        features = dict(spec.get("features", {}))
        for svc, value in spec.get("services", {}).items():
            features["service." + svc] = value
        for key, value in features.items():
            self.feature(vm, key, value)

        for tag in spec.get("tags", []):
            if tag not in vm.tags:                   # admin.vm.tag.Get
                self.step(name, f"add tag {tag}", lambda: vm.tags.add(tag))

    def create(self, name, spec):
        """Create or clone a missing qube. Returns True if it now exists."""
        cls = spec.get("class", "AppVM")
        if "clone_from" in spec:
            src = spec["clone_from"]
            # clone_vm also runs qvm-appmenus locally. Where that tool is
            # missing (a management qube) the clone fails and the library
            # deletes the new qube, unless ignore_errors=True, which turns
            # every copy error into a log line instead.
            lenient = shutil.which("qvm-appmenus") is None
            if lenient:
                self.out(f"note   {name}: no qvm-appmenus here, cloning with "
                         "ignore_errors=True (check the qubesadmin log)")
            ok = self.step(name, f"clone {src} as {cls}",
                           lambda: self.app.clone_vm(src, name, new_cls=cls,
                                                     ignore_errors=lenient))
        else:
            if "label" not in spec:
                raise ValueError(f"{name}: a new qube needs a label")
            ok = self.step(
                name, f"create {cls} (template={spec.get('template')}, "
                      f"label={spec['label']})",
                lambda: self.app.add_new_vm(cls, name, spec["label"],
                                            template=spec.get("template")))
        if self.apply and ok:
            return True
        # Nothing to diff against yet: list the rest of the spec as planned.
        for section in ("prefs", "features", "services"):
            for key, value in spec.get(section, {}).items():
                self.out(f"plan   {name}: {section} {key} = {value!r}")
        for tag in spec.get("tags", []):
            self.out(f"plan   {name}: add tag {tag}")
        return False

    def prop(self, vm, key, value):
        is_default = vm.property_is_default(key)     # admin.vm.property.Get
        if value == DEFAULT:
            if not is_default:
                self.step(vm.name, f"reset {key}", lambda: delattr(vm, key))
            return
        current = wire(current_property(vm, key))    # admin.vm.property.Get
        target = wire(value)
        if current == target and not is_default:
            return
        if key == "template" and current != target and vm.is_running():
            self.failures += 1
            self.out(f"BLOCKED {vm.name}: template {current} -> {target} "
                     "needs the qube halted")
            return
        what = (f"pin {key} = {target!r} (currently the default)"
                if current == target else
                f"set {key}: {current!r} -> {target!r}")
        self.step(vm.name, what, lambda: setattr(vm, key, value))

    def feature(self, vm, key, value):
        current = vm.features.get(key)               # admin.vm.feature.Get
        if value is None:
            if current is not None:
                self.step(vm.name, f"remove feature {key}",
                          lambda: vm.features.__delitem__(key))
            return
        target = feature_wire(value)
        if current != target:
            self.step(vm.name, f"feature {key}: {current!r} -> {target!r}",
                      lambda: vm.features.__setitem__(key, value))


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("state", help="desired-state JSON file")
    parser.add_argument("--apply", action="store_true",
                        help="make the changes (default: print the plan)")
    args = parser.parse_args(argv)

    with open(args.state, encoding="utf-8") as f:
        desired = json.load(f)["qubes"]

    rec = Reconciler(qubesadmin.Qubes(), apply=args.apply)
    changes, failures = rec.run(desired)
    verb = "made" if args.apply else "planned"
    print(f"{changes} change(s) {verb}, {failures} failed or blocked")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
