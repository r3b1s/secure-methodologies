"""Offline tests for reconcile.py, using qubesadmin's own QubesTest fake.

QubesTest answers only the Admin API calls a test scripts in expected_calls,
raises AssertionError on any other call, and records every call made in
actual_calls. So these tests also pin down exactly which calls, and therefore
which qrexec policy lines, the reconciler needs.

Run (needs python3-qubesadmin, or a qubes-core-admin-client checkout on
sys.path; no Qubes system is involved):

    python3 -m unittest test_reconcile.py
"""
import unittest

from qubesadmin.tests import QubesTest

from reconcile import Reconciler, order

OK = b"0\x00"


def vm_list(*names):
    return OK + b"".join(
        f"{n} class=AppVM state=Halted uuid=0\n".encode() for n in names)


def prop(value, typ="str", default=False):
    return OK + f"default={default} type={typ} {value}".encode()


class ReconcileTest(unittest.TestCase):
    def setUp(self):
        self.app = QubesTest()
        self.log = []

    def call(self, dest, method, arg=None, payload=None, reply=OK):
        self.app.expected_calls[(dest, method, arg, payload)] = reply

    def run_rec(self, desired, apply):
        rec = Reconciler(self.app, apply=apply, out=self.log.append)
        return rec.run(desired)

    def writes(self):
        return [c for c in self.app.actual_calls
                if c[1].rsplit(".", 1)[-1] in
                ("Set", "Reset", "Remove", "Create.AppVM")]

    def test_in_sync_reads_only(self):
        self.call("dom0", "admin.vm.List", reply=vm_list("work", "sys-firewall"))
        self.call("work", "admin.vm.property.Get", "netvm",
                  reply=prop("sys-firewall", "vm"))
        self.call("work", "admin.vm.feature.Get", "vm-config.x", reply=OK + b"y")
        self.call("work", "admin.vm.feature.Get", "service.crond", reply=OK + b"1")
        self.call("work", "admin.vm.tag.Get", "managed-by-mgmt", reply=OK + b"1")
        desired = {"work": {"prefs": {"netvm": "sys-firewall"},
                            "features": {"vm-config.x": "y"},
                            "services": {"crond": True},
                            "tags": ["managed-by-mgmt"]}}
        self.assertEqual(self.run_rec(desired, apply=True), (0, 0))
        self.assertEqual(self.writes(), [])

    def test_drift_is_only_planned_without_apply(self):
        self.call("dom0", "admin.vm.List", reply=vm_list("work"))
        self.call("work", "admin.vm.property.Get", "netvm",
                  reply=prop("sys-net", "vm"))
        changes, failures = self.run_rec(
            {"work": {"prefs": {"netvm": "sys-firewall"}}}, apply=False)
        self.assertEqual((changes, failures), (1, 0))
        self.assertEqual(self.writes(), [])
        self.assertIn("set netvm: 'sys-net' -> 'sys-firewall'", self.log[0])

    def test_drift_is_fixed_with_apply(self):
        self.call("dom0", "admin.vm.List", reply=vm_list("work"))
        self.call("work", "admin.vm.property.Get", "netvm",
                  reply=prop("sys-net", "vm"))
        self.call("work", "admin.vm.property.Set", "netvm", b"sys-firewall")
        self.assertEqual(self.run_rec(
            {"work": {"prefs": {"netvm": "sys-firewall"}}}, apply=True), (1, 0))
        self.assertIn(("work", "admin.vm.property.Set", "netvm", b"sys-firewall"),
                      self.app.actual_calls)

    def test_default_value_is_pinned_and_reset_works(self):
        self.call("dom0", "admin.vm.List", reply=vm_list("work"))
        self.call("work", "admin.vm.property.Get", "memory",
                  reply=prop("400", "int", default=True))
        self.call("work", "admin.vm.property.Get", "kernelopts",
                  reply=prop("swiotlb=2048", default=False))
        self.call("work", "admin.vm.property.Set", "memory", b"400")
        self.call("work", "admin.vm.property.Reset", "kernelopts")
        desired = {"work": {"prefs": {"memory": 400, "kernelopts": "@default"}}}
        self.assertEqual(self.run_rec(desired, apply=True), (2, 0))

    def test_create_missing_qube(self):
        # admin.vm.List is called again after the create: give two replies.
        self.call("dom0", "admin.vm.List",
                  reply=[vm_list("fedora-44-xfce"),
                         vm_list("fedora-44-xfce", "dev")])
        self.call("dom0", "admin.vm.Create.AppVM", "fedora-44-xfce",
                  b"name=dev label=purple")
        self.call("dev", "admin.vm.property.Get", "label",
                  reply=prop("purple", "label"))
        self.call("dev", "admin.vm.property.Get", "template",
                  reply=prop("fedora-44-xfce", "vm"))
        desired = {"dev": {"class": "AppVM", "template": "fedora-44-xfce",
                           "label": "purple"}}
        self.assertEqual(self.run_rec(desired, apply=True), (1, 0))

    def test_dry_run_of_missing_qube_creates_nothing(self):
        self.call("dom0", "admin.vm.List", reply=vm_list("fedora-44-xfce"))
        desired = {"dev": {"template": "fedora-44-xfce", "label": "purple",
                           "prefs": {"netvm": None}, "tags": ["t"]}}
        self.assertEqual(self.run_rec(desired, apply=False), (1, 0))
        self.assertEqual(self.writes(), [])
        self.assertEqual(self.log[1:], ["plan   dev: prefs netvm = None",
                                        "plan   dev: add tag t"])

    def test_dry_run_of_clone_creates_nothing(self):
        self.call("dom0", "admin.vm.List", reply=vm_list("fedora-44-xfce"))
        desired = {"tpl-dev": {"class": "TemplateVM",
                               "clone_from": "fedora-44-xfce"}}
        self.assertEqual(self.run_rec(desired, apply=False), (1, 0))
        self.assertEqual(self.writes(), [])
        self.assertTrue(any("clone fedora-44-xfce as TemplateVM" in line
                            for line in self.log))

    def test_feature_removal_and_false_service(self):
        self.call("dom0", "admin.vm.List", reply=vm_list("work"))
        self.call("work", "admin.vm.feature.Get", "old", reply=OK + b"x")
        self.call("work", "admin.vm.feature.Remove", "old")
        # A missing feature is an exception reply, which features.get() maps to None.
        self.call("work", "admin.vm.feature.Get", "service.cups",
                  reply=b"2\x00QubesFeatureNotFoundError\x00\x00no such feature\x00")
        self.call("work", "admin.vm.feature.Set", "service.cups", b"")
        desired = {"work": {"features": {"old": None},
                            "services": {"cups": False}}}
        self.assertEqual(self.run_rec(desired, apply=True), (2, 0))

    def test_policy_denial_is_a_failure_not_a_crash(self):
        self.call("dom0", "admin.vm.List", reply=vm_list("work"))
        # An empty reply is what qubesd sends when it refuses a call.
        self.call("work", "admin.vm.property.Get", "netvm", reply=b"")
        changes, failures = self.run_rec(
            {"work": {"prefs": {"netvm": "sys-firewall"}}}, apply=True)
        self.assertEqual((changes, failures), (0, 1))
        self.assertIn("QubesPropertyAccessError", self.log[-1])

    def test_template_change_blocked_while_running(self):
        self.call("dom0", "admin.vm.List", reply=vm_list("work"))
        self.call("work", "admin.vm.property.Get", "template",
                  reply=prop("fedora-43-xfce", "vm"))
        self.call("work", "admin.vm.CurrentState",
                  reply=OK + b"power_state=Running mem=400")
        self.assertEqual(self.run_rec(
            {"work": {"template": "fedora-44-xfce"}}, apply=True), (0, 1))
        self.assertTrue(self.log[-1].startswith("BLOCKED"))

    def test_order_puts_dependencies_first(self):
        desired = {"app": {"template": "tpl", "prefs": {"netvm": "sys-x"}},
                   "sys-x": {"template": "tpl"},
                   "tpl": {"class": "TemplateVM"}}
        self.assertEqual(order(desired), ["tpl", "sys-x", "app"])


if __name__ == "__main__":
    unittest.main()
