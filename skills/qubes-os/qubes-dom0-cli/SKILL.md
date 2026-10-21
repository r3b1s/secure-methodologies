---
name: qubes-dom0-cli
description: Reference for the Qubes OS command-line tools that exist only in dom0 (the admin qube) — qvm-* lifecycle/inspection/configuration tools, qubes-prefs, qvm-run, devices, storage, templates, backups, updates, qrexec policy tools (qubes-policy, qubes-policy-lint, qrexec-client, qubesd-query), Salt (qubesctl), and the low-level qubesdb/xl/xenstore layer. Use when writing or running anything in dom0, writing a dom0 provisioning script, managing qubes from dom0 (create, clone, prefs, features, services, firewall, devices, volumes, templates, backups), editing qrexec policy, or when a command must run "from dom0". For tools that run inside other qubes, use qubes-vm-cli instead.
license: MIT
metadata:
  verified-on: "Qubes OS R4.3.2"
---

# Qubes OS CLI — dom0 only

Verified on **Qubes R4.3.2** dom0 (2026-10): each tool's `--help` was
captured on a real install, and flags below match it. Sources of truth:

- Upstream index: `user/reference/tools.rst` in
  https://github.com/QubesOS/qubes-doc (rendered at
  https://doc.qubes-os.org/en/latest/user/reference/tools.html). Its dom0
  section points to the `core-admin` and `core-admin-client` manpages,
  `qvm-appmenus` and `qvm-xkill`.
- Manpages for the `qvm-*` tools:
  https://github.com/QubesOS/qubes-core-admin-client/tree/main/doc/manpages
- qrexec and policy:
  https://github.com/QubesOS/qubes-core-qrexec and
  https://doc.qubes-os.org/en/latest/developer/services/qrexec.html
- The live system: `<tool> --help` and `man <tool>` in dom0 (but see §11
  for tools that ignore `--help`).

When this file disagrees with the installed tool, the installed tool wins.

## 1. What dom0 is, and what that means for every command

- dom0 is the **AdminVM**: it runs `qubesd`, the Xen toolstack, the GUI
  daemon and the qrexec policy daemon. It has **no network**. Packages come
  only through `qubes-dom0-update` (fetched via the UpdateVM).
- The `qvm-*` tools are thin **frontends to `qubesd`** over the admin API
  (`admin.*` qrexec calls, see `/etc/qubes-rpc/admin.*`). Anything a
  `qvm-*` tool does, `qubesd-query` can do raw (§9).
- They run as the **normal dom0 user** (a member of group `qubes`); no
  `sudo` needed. Exceptions that need root: `qubes-policy` (policy
  editing), `qubes-fwupdmgr`, installing with `qubes-dom0-update`, and
  anything writing `/etc/qubes*`.
- Package owners (R4.3.2): `qubes-core-admin-client` (33 `qvm-*` tools),
  `qubes-core-qrexec` / `qubes-core-qrexec-dom0` (qrexec + policy),
  `qubes-core-dom0` / `qubes-core-dom0-linux` (`qubesd`, `qubes-dom0-update`,
  `qubes-prepare-vm-kernel`…), `qubes-manager` / `qubes-desktop-linux-*`
  (GUI apps, `qvm-appmenus`, `qvm-xkill`, `qubes-i3*`).
- In a domU the same `qvm-*` names only work if `qubes-core-admin-client`
  is installed there **and** dom0's admin policy grants it (a management
  qube). Normal qubes don't have them; see qubes-vm-cli.

## 2. Conventions every `qvm-*` tool shares

- Common flags: `--verbose/-v`, `--quiet/-q`, `--help/-h`, `--version`.
- Multi-qube tools take `VMNAME ...` plus `--all` and `--exclude NAME`
  (repeatable): `qvm-shutdown --all --exclude sys-net --wait`.
- Put `--` before qube names that come from variables:
  `qvm-shutdown --wait -- "$vm"`.
- Exit status is the contract for scripts; prefer predicates over parsing:
  `qvm-check --quiet --running -- "$vm"`.
- Property/feature values: booleans accept `True/true/on/1` and
  `False/false/off/0`; a qube-typed property takes a qube name, or `''`
  for none (e.g. `qvm-prefs work netvm ''` = offline).

## 3. Inspect

```bash
qvm-ls                                    # human table (format "simple")
qvm-ls --raw-list                         # names only, one per line
qvm-ls --raw-data --fields NAME,STATE,CLASS,IP   # pipe-separated, for scripts
qvm-ls --running --class AppVM            # filters: --running/--paused/--halted,
                                          #   --class, --label, --tags, --netvm-is,
                                          #   --template-source, --features K=V, --prefs K=V
qvm-ls --tree                             # netvm hierarchy
qvm-ls --format network                   # presets: disk full kernel network prefs simple
qvm-check --quiet --running sys-net       # also --paused --template --networked
qvm-prefs work                            # all properties of a qube
qubes-prefs                               # all global properties
qvm-features work                         # all features; qvm-features work NAME → one
qvm-service work                          # list services (default action, also -l)
qvm-tags work list                        # tags; `list TAG` exits 0/1 if set
qvm-notes work --print
```

`qvm-ls --help-formats` / `--help-columns` list the presets and columns.
Columns that are handy in scripts: `NAME`, `STATE`, `CLASS`, `IP`,
`LABEL`, `TEMPLATE`, `NETVM`.

## 4. Lifecycle

```bash
qvm-create --template fedora-44-xfce --label blue work     # class AppVM by default
qvm-create --class TemplateVM --label black my-template
qvm-create --standalone --label red sa                      # = --class StandaloneVM
qvm-create --disp --template dvm-foo sys-foo                # named disposable (DispVM);
                                                            #   --disp alone implies --label red
qvm-create --property memory=800 --property vcpus=2 -t fedora-44-xfce -l green w2
qvm-clone fedora-44-xfce tpl-foo          # keeps the class; -C to change it, -P POOL
qvm-start --skip-if-running work
qvm-shutdown --wait --timeout 60 work     # graceful; kills after timeout
qvm-kill work                             # immediate, no shutdown sequence
qvm-pause work / qvm-unpause work         # --suspend/-S for S3; paused qubes die at host shutdown
qvm-remove --force work                   # irreversible; prompts without --force
```

- `--label` is required for `qvm-create`, except with `--disp`.
- `qvm-clone` refuses while the source is running; shut it down first.
- `qvm-shutdown --force` only overrides the "other qubes depend on it"
  check (e.g. a netvm); it does not change how the qube shuts down.
  `--dry-run` with `--wait` is useful in scripts.
- `qvm-start --cdrom IMAGE | --hddisk IMAGE | --drive hd:/cdrom:...`
  attaches media for that boot only.

## 5. Configure a qube

### Properties — `qvm-prefs`, `qubes-prefs`

```bash
qvm-prefs work netvm sys-firewall
qvm-prefs work netvm ''                   # no network
qvm-prefs --default work netvm            # back to the default (also -D)
qvm-prefs --hide-default work             # only what was set explicitly
qubes-prefs default_netvm sys-firewall    # global defaults
```

Per-qube properties (R4.3.2, AppVM): `audiovm autostart backup_timestamp
bootmode debug default_dispvm default_user devices_denied dns gateway
gateway6 guivm icon include_in_backups installed_by_rpm ip ip6 kernel
kernelopts keyboard_layout klass label mac management_dispvm maxmem memory
name netvm provides_network qid qrexec_timeout shutdown_timeout start_time
stubdom_mem stubdom_uuid stubdom_xid template template_for_dispvms
updateable uuid vcpus virt_mode visible_gateway visible_gateway6 visible_ip
visible_ip6 visible_netmask xid`. `ip` is settable (pin an address; Qubes
does not check for clashes).

Global properties: `check_updates_vm clockvm default_audiovm default_dispvm
default_guivm default_kernel default_netvm default_pool default_pool_kernel
default_pool_private default_pool_root default_pool_volatile
default_qrexec_timeout default_shutdown_timeout default_template
management_dispvm stats_interval updatevm`.

`--help-properties` prints descriptions. `--get/-g` and `--set/-s` are
accepted but ignored (old-script compatibility).

### Features, services, tags, notes

```bash
qvm-features work NAME VALUE              # set; qvm-features --unset work NAME (or -D)
qvm-features sys-foo vm-config.KEY VALUE  # readable in the qube: qubesdb-read /vm-config/KEY
qvm-service work cups on                  # = feature service.cups=1 → /run/qubes-service/cups
qvm-service --enable work NAME / --disable / --unset
qvm-tags work add trusted                 # tags are what qrexec policy matches with @tag:NAME
qvm-tags work del trusted
qvm-notes work --set 'text' / --append 'text' / --import FILE / --delete
```

- A feature without the `service.` prefix does **not** create a
  `/run/qubes-service/` flag; use `qvm-service` for service toggles.
- Features are also how qubes report capabilities to dom0
  (`qvm-features-request` in the qube). Set only features that a doc or
  extension defines.

### Firewall — `qvm-firewall`

```bash
qvm-firewall work list
qvm-firewall work add accept dsthost=example.com proto=tcp dstports=443
qvm-firewall work add action=accept specialtarget=dns
qvm-firewall work add drop                # final rule: drop everything else
qvm-firewall work del --rule-no 2
qvm-firewall work reset                   # back to accept-all
```

Matches: `action` (accept/drop), `dsthost` (IP, CIDR or hostname; `dst4`
and `dst6` are synonyms), `proto` (tcp/udp/icmp), `dstports` (`443` or
`1200-1400`), `icmptype`, `specialtarget=dns`, `expire` (epoch or `+secs`),
`comment=...`. `add --before N` inserts. The rules are enforced by the
qube's **netvm** (its `qubes-firewall` service), so a qube with
`netvm=''` ignores them.

## 6. Devices and storage

```bash
qvm-device --list-device-classes          # block usb pci mic …
qvm-usb list                              # = qvm-device usb list; also qvm-block, qvm-pci
qvm-usb attach work sys-usb:2-1           # BACKEND:DEVICE_ID; --ro, --option K=V
qvm-usb detach work sys-usb:2-1
qvm-pci list
qvm-pci assign --required sys-net dom0:00_14.0   # persistent; --ask, --port|--device
qvm-pci unassign sys-net dom0:00_14.0
qvm-block attach --ro work dom0:loop0
```

R4.3 split attachment into `attach` (now) and `assign` (persistent rule,
optionally `--required` to block start without it). `list --assignments`
shows rules. PCI backends are always `dom0`.

```bash
qvm-volume list work                      # VM:VOLUME = work:root, work:private, work:volatile
qvm-volume info work:private
qvm-volume resize work:private 20GiB      # grow; shrinking needs --force
qvm-volume revert work:private            # previous revision (see `info` revisions)
qvm-volume config work:private revisions_to_keep 2
qvm-volume import work:private image.img
qvm-pool --list                           # also -i NAME, -a NAME DRIVER -o k=v, -r NAME, -s NAME -o
qvm-pool --help-drivers
```

R4.3.2 `qvm-pool` uses the flag interface shown above (`qvm-pool-legacy`
is the same).

## 7. Run code and move data into qubes

```bash
qvm-run work 'xterm'                      # GUI app; returns once started
qvm-run --pass-io work 'cat /etc/os-release'      # stdio connected; exit code propagated
qvm-run --pass-io --user root work 'dnf -y upgrade'   # --user/-u only from dom0
qvm-run --pass-io --no-autostart work 'uptime'        # fail instead of starting it
qvm-run --service work qubes.StartApp+firefox         # call a qrexec service
qvm-run --dispvm=dvm-foo --service qubes.StartApp+xterm
qvm-run --pass-io --no-shell work /usr/bin/id         # exec, no shell parsing
qvm-run --all --pass-io 'uptime'          # every running qube
qvm-run --pass-io -u root tpl -- bash -s <<'EOF'     # push a script, the dom0 idiom
set -euo pipefail
...
EOF
qvm-copy-to-vm work file1 dir/            # → work:~/QubesIncoming/dom0/
qvm-move-to-vm work file
```

- `qvm-run` starts (or unpauses) the qube unless `--no-autostart`.
- Output is filtered for terminal escapes when stdout is a terminal;
  `--no-filter-escape-chars` disables that (dangerous on a terminal).
- `qvm-copy` and `qvm-move` are **not supported in dom0**; use the
  `-to-vm` forms.
- **Never copy data from a qube into dom0** (`qvm-run --pass-io vm 'cat
  x' > file` and similar). dom0 must not parse untrusted data. Push code
  in, read only what you control.

## 8. Templates and updates

```bash
qvm-template list --available             # also --installed, --upgrades, --extras;
                                          #   --machine-readable(-json) for scripts
qvm-template install fedora-44-xfce       # --pool, --skip-start, --nogpgcheck (don't)
qvm-template upgrade fedora-44-xfce
qvm-template remove old-template          # purge = remove + its qubes
qvm-template repolist                     # repos: /etc/qubes/repo-templates/*.repo
qubes-vm-update --templates               # update all templates (the CLI updater)
qubes-vm-update --targets work,tpl-foo --force-update
qubes-vm-update --apply-to-sys            # restart service qubes whose template changed
qubes-dom0-update                         # update dom0
sudo qubes-dom0-update PACKAGE            # install a package into dom0
qubes-dom0-update --check-only
```

- `qubes-vm-update` defaults: `--all` targets (not dom0),
  `--update-if-stale 7`, `--no-apply`; `--dry-run` shows the plan.
  `--signal-no-updates` makes "nothing to do" exit 100.
- `qubes-dom0-update` options with values must be glued:
  `--action=reinstall`, `--enablerepo=foo` (not `--enablerepo foo`).
- `qubesctl` drives Salt: `sudo qubesctl --skip-dom0 --targets tpl-foo
  state.highstate`, `sudo qubesctl state.sls NAME`.

## 9. qrexec policy and RPC from dom0

- Policy lives in `/etc/qubes/policy.d/*.policy`, read in filename order;
  **first matching line wins**, no match = deny. Format:
  `SERVICE ARGUMENT SOURCE TARGET ACTION [OPTIONS]`, e.g.
  `my.Service * work dom0 allow`.
- The TARGET column must match what the caller asks for: `@default`
  only matches callers that ask for `@default`; to redirect them, use
  `@default allow target=X`. A caller that names `dom0` needs `dom0` in
  that column.
- dom0's policy daemon reads the files on every call; no restart.
- Services dom0 provides live in `/etc/qubes-rpc/` (`admin.*`, `policy.*`,
  `qubes.*`, plus your own). Each file is the program run for that
  service name.

```bash
qubes-policy-lint -s my.policy           # check a file before installing it
sudo qubes-policy -l                      # list policy files (needs root)
sudo qubes-policy -g 90-default           # print one
sudo qubes-policy -r 30-mine < file.policy   # replace via the API; -d removes
qrexec-policy-graph --service qubes.Filecopy --output out.dot  # who can call what
qrexec-client -d work user:'id'           # low-level dom0→qube exec (qvm-run is the friendly one)
qubesd-query --empty dom0 admin.vm.List dom0 | tr '\0' '\n'   # raw admin API call
```

`qubesd-query SRC METHOD DEST [ARG]` returns `0\0` + payload on success;
`--fail` makes errors a non-zero exit.

## 10. Low level (read-mostly)

```bash
qubesdb-read -d work /qubes-ip            # read a qube's qubesdb from dom0 (-d only in dom0)
qubesdb-list -d work /                    # its keys
xl list                                   # Xen domains, IDs, memory
xl dmesg | tail
xenstore-ls /local/domain/0 | head
```

Changing anything with `xl` or `xenstore-*` bypasses `qubesd` and leaves
its state inconsistent. Use them to look, and do changes with `qvm-*`.

Other dom0-only tools: `qvm-backup` / `qvm-backup-restore` (backups are
always encrypted; `--dest-vm` writes into a qube; `--verify-only`;
`--paranoid-mode` restores through a disposable), `qubes-hcl-report`,
`qubes-prepare-vm-kernel`, `qvm-console-dispvm` (text console through a
disposable), `qubes-vm-boot-from-device`, `qvm-appmenus` /
`qvm-sync-appmenus` (app menu entries), `qvm-start-daemon` (GUI/audio
daemons), `qubes-i3*` and `qubes-input-sender` (desktop integration, e.g. for
i3). GUI apps: `qubes-qube-manager`,
`qubes-global-config`, `qubes-template-manager`, `qubes-vm-settings`,
`qubes-new-qube`, `qubes-update-gui`, `qubes-policy-editor-gui`.

## 11. Gotchas

- **Some tools ignore `--help` and act.** `qvm-console` opens a console,
  `qvm-sync-clock` tries to set the clock, `qvm-xkill` waits for a window
  to kill (needs `DISPLAY`), `qubes-policy-admin` is a qrexec service
  handler, not a CLI. Read `man TOOL` for these instead of probing.
- **No `DISPLAY` in non-GUI sessions** (e.g. a dom0 shell reached through
  a qrexec service). GUI-touching commands need `DISPLAY=:0` and are better
  run from a dom0 terminal.
- **Paused qubes are killed** when the host shuts down.
- **Changes to a template's root** reach its qubes only after the template
  shuts down and each qube restarts.
- **`--label` is a trust colour**, not decoration; window borders show it.
- **Removing a qube** that others reference (`template`, `netvm`,
  `default_dispvm`) fails; repoint the references first.
- **dom0 has no git and no network**: bring code in through a qube
  (`qvm-run --pass-io vm 'tar -cf - repo' | tar -xf -`), and only for code
  you trust, such as your own dotfiles.

Companion skills from the same collection, installed separately:
`qubes-vm-cli` (tools inside qubes) and `qubes-disposable-vms` (disposable
patterns and dom0 provisioning scripts).
