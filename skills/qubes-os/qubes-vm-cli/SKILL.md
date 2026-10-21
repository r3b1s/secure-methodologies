---
name: qubes-vm-cli
description: Reference for the Qubes OS command-line tools available inside qubes other than dom0 (AppVMs, templates, disposables, standalones) — qvm-copy/qvm-move, qvm-open-in-vm/qvm-open-in-dvm, qvm-run-vm, qrexec-client-vm, qvm-connect-tcp, qvm-convert-pdf/img, qvm-features-request, qubesdb-read and friends, service flags, and the qrexec services a qube provides. Use when writing scripts or rc.local hooks that run inside a qube, moving files or calling services between qubes, reading a qube's own config (IP, name, vm-config features, services), or debugging a "Request refused" / denied qrexec call from a qube. For tools that only exist in dom0 (qvm-create, qvm-prefs, policy editing…), use qubes-dom0-cli instead.
license: MIT
metadata:
  verified-on: "Qubes OS R4.3.2"
---

# Qubes OS CLI — inside qubes (not dom0)

Verified on **Qubes R4.3.2**, in a Fedora 44 AppVM (2026-10):
the tool list, the `--help` output, the qubesdb keys and the qrexec services
below come from that qube. Debian and other Linux templates ship the same
agent tools from the same upstream packages. Sources of truth:

- Upstream index: `user/reference/tools.rst` (DomU section) in
  https://github.com/QubesOS/qubes-doc (rendered at
  https://doc.qubes-os.org/en/latest/user/reference/tools.html).
- Manpages for the agent tools:
  https://github.com/QubesOS/qubes-core-agent-linux/tree/main/doc/vm-tools
- `qrexec-client-vm`:
  https://github.com/QubesOS/qubes-core-qrexec/blob/main/agent/qrexec-client-vm.rst

When this file disagrees with the installed tool, the installed tool wins.

## 1. The model: a qube asks, dom0 decides

- A qube holds no power over other qubes. Every cross-qube action is a
  **qrexec call**: the qube asks dom0 to run SERVICE in TARGET, dom0
  evaluates `/etc/qubes/policy.d/` (allow, deny or ask), and only then
  connects the two ends over vchan. There is no network path involved.
- So every tool below can be **denied by policy**, and a denial shows up in
  the qube as `Request refused` (exit **126** from `qrexec-client-vm`) and
  in dom0 as a "Denied: SERVICE from X to Y" notification.
- The tools come from the agent packages: `qubes-core-agent` (copy, open,
  run, converters' front ends…), `qubes-core-qrexec` /
  `qubes-core-qrexec-vm` (`qrexec-client-vm`), `qubes-db` (`qubesdb-*`),
  `qubes-gui-agent`, `qubes-pdf-converter`, `qubes-img-converter`,
  `qubes-gpg-split`.
- `qvm-create`, `qvm-prefs`, `qvm-ls` and the other admin tools **do not
  exist here**. A qube can only use them with `qubes-core-admin-client`
  installed **and** an admin-API policy grant in dom0 (a management qube).

## 2. Read your own configuration (qubesdb)

dom0 publishes each qube's settings into its qubesdb at start. Reading it
is the right way for a script to learn about its qube:

```bash
qubesdb-read /name                        # this qube's name
qubesdb-read /qubes-vm-type               # AppVM, TemplateVM, DispVM, StandaloneVM
qubesdb-read /qubes-ip                    # also /qubes-gateway, /qubes-netmask,
                                          #   /qubes-primary-dns, /qubes-secondary-dns, /qubes-mac
qubesdb-read /vm-config/KEY               # set in dom0 with: qvm-features QUBE vm-config.KEY VALUE
qubesdb-read -e fallback /vm-config/KEY   # default if missing (or check the exit code)
qubesdb-list /                            # all keys
qubesdb-list /vm-config/
qubesdb-watch /qubes-ip                   # block until it changes (-n N events)
```

Top-level keys seen on R4.3.2: `default-user keyboard-layout name
qubes-base-template qubes-block-devices qubes-debug-mode qubes-gateway
qubes-gui-enabled qubes-ip qubes-keyboard qubes-mac qubes-netmask
qubes-primary-dns qubes-secondary-dns qubes-service/* qubes-timezone
qubes-usb-devices qubes-vm-persistence qubes-vm-type qubes-vm-updateable
type vm-config/*`.

- `qubesdb-read` exits non-zero when the key is missing, which makes
  `x=$(qubesdb-read /vm-config/foo) || exit 0` a clean "feature not set"
  guard.
- All `qubesdb-*` commands are one binary: `-c read|write|rm|multiread|
  list|watch`, `-f` full paths, `-r` raw values, `-q` quiet. They reject
  `--help`; use `-h`.

**Service flags.** `qvm-service QUBE NAME on` in dom0 shows up as the file
`/run/qubes-service/NAME` (and qubesdb `/qubes-service/NAME`). Gate units
on it with `ConditionPathExists=/run/qubes-service/NAME`.

## 3. Move files between qubes

```bash
qvm-copy file dir/                        # prompts for the destination qube
qvm-move file                             # copy, then delete the local original
qvm-copy-to-vm work file                  # name the destination yourself (scripts)
qvm-move-to-vm work file
qvm-copy --without-progress --ignore-symlinks dir/
```

- Files land in `~/QubesIncoming/<SOURCE-QUBE>/` in the destination.
  Directories copy recursively; symlinks are copied unless
  `--ignore-symlinks`.
- Each transfer is a `qubes.Filecopy` call, so policy decides (default:
  ask).
- In dom0 only the `-to-vm` forms work.

## 4. Open files and URLs elsewhere

```bash
qvm-open-in-vm work-web https://example.com     # named qube
qvm-open-in-vm @default file.pdf                # let policy pick the target
qvm-open-in-dvm untrusted.pdf                   # a new disposable, every time
qvm-open-in-dvm --view-only -- report.odt       # changes are not sent back
```

These call `qubes.OpenInVM` / `qubes.OpenURL`. Without `--view-only`, an
edited file is copied back when the viewer closes.

## 5. Run commands and services in other qubes

### `qvm-run-vm` — a shell command in another qube

```bash
qvm-run-vm work 'ls ~'                    # qubes.VMShell; args joined, run with bash -c
qvm-run-vm --no-gui work 'make'
qvm-run-vm @dispvm 'curl -s example.com'  # new disposable ($dispvm also works)
```

Unlike dom0's `qvm-run`, it does **not** propagate the remote exit code and
does **not** filter terminal escapes. Use it interactively, and use
`qrexec-client-vm` when a script needs the exit status.

### `qrexec-client-vm` — the raw RPC client

```bash
qrexec-client-vm TARGET SERVICE[+ARG] [LOCAL_PROGRAM [ARGS...]]
qrexec-client-vm work qubes.StartApp+firefox
qrexec-client-vm @default my.Service            # let policy pick the target
qrexec-client-vm @dispvm:dvm-foo qubes.VMShell <<< 'id'
qrexec-client-vm dom0 my.Service                # a service that dom0 itself provides
echo data | qrexec-client-vm work my.Service    # stdin/stdout are the pipe
qrexec-client-vm work my.Service /usr/bin/my-client   # or connect a local program
```

- **TARGET**: a qube name, `@default` (policy decides), `@dispvm` or
  `@dispvm:TEMPLATE`. The manpage still lists the older `$default` /
  `$dispvm` spellings (also accepted) and an empty string.
- **Policy matching**: dom0's policy TARGET column must match what you
  ask for. Asking for `dom0` needs a rule with target `dom0`; a rule with
  `@default ... target=dom0` only matches callers that ask for `@default`.
- **Exit status**: the remote service's status, or the local program's
  when one is given; **126** = denied by policy; **125** = the call failed
  for another reason (configuration, resources); 128+N for a signal.
- Useful options: `-p DATA` (`--prefix-data`) sends DATA before stdin;
  `--buffer-size=N`; `-t`/`-T` filter control characters on
  stdout/stderr (the default when they are terminals).
- Service names are up to 63 characters (`[A-Za-z0-9._-]`, `+` for the
  argument); targets up to 31.

### `qvm-connect-tcp` — a TCP port from another qube, without networking

```bash
qvm-connect-tcp 2222:work:22              # localhost:2222 here → work port 22
qvm-connect-tcp ::22                      # port 22 → @default (policy decides), port 22
ssh -p 2222 user@localhost
```

Uses `qubes.ConnectTCP` (policy argument `+PORT`). It binds on localhost
only. Expose it more widely with your own socket unit that runs
`qrexec-client-vm TARGET qubes.ConnectTCP+PORT`.

## 6. Disarm untrusted documents

```bash
qvm-convert-pdf scan.pdf                  # → scan.trusted.pdf next to it; the original
                                          #   moves to ~/QubesUntrustedPDFs/
qvm-convert-pdf --in-place scan.pdf       # → scan.trusted.pdf; the original is deleted
qvm-convert-pdf -a ~/originals -r 150 -b 4 *.pdf
qvm-convert-pdf -p PASSWORD encrypted.pdf
qvm-convert-img in.png out.png
```

Pages are rendered to bitmaps in a disposable and rebuilt, which destroys
any embedded exploit and also the text layer. R4.3.2's `qvm-convert-pdf`
has `-b/--batch`, `-a/--archive`, `-i/--in-place`, `-r/--resolution`
(75–4800, default 300) and `-p/--password`. It has **no** OCR option, and
`qvm-convert-file` is not installed by default.

## 7. Talk to dom0

```bash
qvm-features-request supported-service.foo=1 --commit   # report a capability to dom0
qubes-gpg-client --list-keys              # split GPG: keys live in another qube (QUBES_GPG_DOMAIN)
```

- `qvm-features-request` is how templates advertise features to dom0
  (dom0 decides what to accept). Without `--commit` it only stages the
  request in qubesdb.
- Present in a qube but **not usable without admin-API access**:
  `qvm-appmenus`, `qvm-sync-appmenus`, `qvm-xkill` (they ship with
  `qubes-desktop-linux-common` for GUI qubes). `qvm-sync-clock` needs root
  and is run by the system.

## 8. Services this qube offers

Programs in `/etc/qubes-rpc/` (from the template) and
`/usr/local/etc/qubes-rpc/` (per-qube, persistent in an AppVM) are the
services other qubes and dom0 can call **into** this qube, policy
permitting. A Fedora 44 AppVM on R4.3.2 ships: `qubes.Filecopy`,
`qubes.OpenInVM`, `qubes.OpenURL`, `qubes.VMShell`, `qubes.VMRootShell`,
`qubes.VMExec`, `qubes.VMExecGUI`, `qubes.VMRootExec`, `qubes.StartApp`,
`qubes.ConnectTCP`, `qubes.PdfConvert`, `qubes.Gpg`, `qubes.GpgImportKey`,
`qubes.USB`, `qubes.USBAttach`, `qubes.USBDetach`, `qubes.Backup`,
`qubes.Restore`, `qubes.GetAppmenus`, `qubes.SyncAppMenus`,
`qubes.UpdatesProxy`, `qubes.SaltLinuxVM`, `qubes.ShowInTerminal`,
`qubes.WaitForSession`, `qubes.SetDateTime`, `qubes.ResizeDisk`, and more.

To add one: put an executable at `/usr/local/etc/qubes-rpc/my.Service`
(AppVM) or `/etc/qubes-rpc/my.Service` (template). Its stdin/stdout
connect to the caller, `$QREXEC_REMOTE_DOMAIN` names the caller, and the
`+ARG` arrives as `$1` / `$QREXEC_SERVICE_ARGUMENT`. Then add a policy
line in dom0.

## 9. Gotchas

- **`Request refused` / exit 126 means policy, not a broken service.**
  Check the policy's TARGET column first (§5), then the source name and
  the service name spelling.
- **Some tools ignore `--help` and act**: `qvm-sync-clock` tries to set
  the clock, and `qvm-xkill` waits for a window to kill. `qubesdb-*`
  rejects `--help` (use `-h`). Prefer `man TOOL`.
- **AppVM root is reset at every boot.** Only `/home`, `/rw` and
  `/usr/local` persist. Install packages and system services in the
  template, and per-qube hooks in `/rw/config/`.
- **Templates are offline**: downloads go through the updates proxy at
  `127.0.0.1:8082` (dnf/apt are pre-configured; set
  `https_proxy=http://127.0.0.1:8082` for curl/git), and only when the
  `updates-proxy-setup` service is on.
- **`qvm-run-vm` loses exit codes**; script with `qrexec-client-vm`.
- **Incoming files are untrusted**: anything in `~/QubesIncoming/` came
  from another qube; treat it like a download.

Companion skills from the same collection, installed separately:
`qubes-dom0-cli` (dom0-only tools and policy editing) and
`qubes-disposable-vms` (disposable patterns, `/rw` hooks, bind-dirs).
