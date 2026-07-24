---
name: polarfire-soc-setup
description: >-
  Set up a PolarFire SoC Discovery Kit embedded firmware project:
  WSL tools, Yocto SDK build, SSH access, and development workflow.
  Covers host/WSL packages, Yocto manifest sync, populate_sdk build, 
  SSH client troubleshooting (Windows vs. WSL), and project structure.
metadata:
  pattern: tool-wrapper
  secondary: "hybrid: long SKILL body includes checklist / scaffold sections like a generator"
  version: 1.0
  domain: embedded-firmware
  board: PolarFire SoC Discovery Kit (MPFS095T)
  os_target: Linux (embedded on RISC-V)
  build_host: WSL (Ubuntu 24.04)
  triggers:
    - setup polarfire, polarfire firmware, yocto sdk install
    - embedded development, discovery kit, pat system
    - wsl yocto, arm/risc-v cross-compile, ssh board
---

# PolarFire SoC Discovery Kit Setup

**Goal:** Bootstrap a **plan-first** embedded firmware project on **PolarFire SoC Discovery Kit (MPFS095T)** with WSL cross-compilation, Yocto SDK, and board access.

## Prerequisites

- **Windows 10/11** with **WSL2** + **Ubuntu 24.04** (or similar)
- **~50 GB free disk** in WSL (for Yocto build artifacts)
- **Network access** to GitHub (repo manifests, BSP)
- **Board on same subnet** as dev machine (or port-forwarded SSH)

## Quick setup (5 steps)

### 1. Install WSL build dependencies

From **WSL Ubuntu** (as root or with `sudo`):

```bash
export DEBIAN_FRONTEND=noninteractive
apt-get update && apt-get install -y \
  build-essential cmake ninja-build pkg-config \
  gawk wget git diffstat unzip texinfo \
  python3 python3-pip python3-pexpect xz-utils \
  cpio socat chrpath flex bison \
  libncurses-dev libssl-dev device-tree-compiler \
  gcc-riscv64-unknown-elf binutils-riscv64-unknown-elf \
  gdb gdb-multiarch openocd clang llvm repo
```

**Verify:**
```bash
riscv64-unknown-elf-gcc --version
cmake --version
openocd --version
```

### 2. Sync PolarFire Yocto (2025.03 release)

From **WSL**:

```bash
mkdir -p ~/yocto-mpfs-2025.03
cd ~/yocto-mpfs-2025.03
repo init -u https://github.com/polarfire-soc/polarfire-soc-yocto-manifests.git \
  -b 2025.03 -m default.xml
repo sync -j4
```

Expect **~10 GB** download, **~15–30 min** depending on network.

### 3. Configure BSP for Discovery Kit

From **same WSL dir**:

```bash
source meta-polarfire-soc-yocto-bsp/polarfire-soc_yocto_setup.sh \
  -b build -m mpfs-disco-kit
```

This initializes **OpenEmbedded** and **bitbake** layers for the board.

### 4. Build the Yocto SDK (populate_sdk)

**Important:** This takes **2–4 hours** and uses **20–30 GB** disk.

```bash
source openembedded-core/oe-init-build-env build
bitbake core-image-minimal-dev -c populate_sdk
```

**Monitor progress:**
```bash
tail -f build/bitbake.log  # optional; running jobs shown as 'NOTE:'
```

When done, check **`build/tmp/deploy/sdk/*.sh`** exists.

### 5. Install SDK to `/opt` (WSL)

From **project repo** in WSL:

```bash
bash scripts/wsl/finish_yocto_sdk_install.sh
```

This:
- Finds the generated `.sh` installer
- Runs it with `sudo` into `/opt/oecore-x86_64`
- Prints the `environment-setup-*` path to **source** before builds

**Example output:**
```
Environment script(s):
/opt/oecore-x86_64/environment-setup-riscv64-oe-linux
```

Store that path; you'll source it in `./scripts/build.sh`.

---

## SSH to board

### Linux / WSL (working ✓)

```bash
wsl -d Ubuntu -- ssh -o StrictHostKeyChecking=accept-new root@192.168.8.100 "uname -a"
```

### Windows OpenSSH (MAC negotiation issue ✗)

Windows OpenSSH 9.5 and board OpenSSH 9.6 have a **MAC mismatch**. Workarounds:

1. **Use WSL SSH** (recommended)
2. **Add to `~/.ssh/config`** on Windows:
   ```
   Host 192.168.8.100
     StrictKeyExchange no
   ```
3. **Board serial console** — check `/var/log/auth.log` for auth errors

---

## Project structure & workflow

See **`docs/workflow/WORKFLOW.md`** for full plan-first embedded dev loop:

| Step | Command | Result |
|------|---------|--------|
| **Edit** | `${EDITOR} firmware/foo.c` | Source changes |
| **Build** | `. env-setup.sh && ./scripts/build.sh` | `build/app` binary |
| **Deploy** | (wired in `build.sh` via `scp` from WSL) | Binary on board |
| **Run** | `wsl -d Ubuntu -- ssh root@192.168.8.100 ./app` | Live test |
| **Verify** | Check logs / output / LED / ADC / etc. | Pass/fail criteria |

---

## Troubleshooting

### `populate_sdk` hangs or fails

- **Disk full** — Check `df -h` in WSL; need **20–30 GB** under `build/tmp/sstate-cache/`.
- **Network** — Yocto fetches many tarballs; use **`bitbake … -c populate_sdk 2>&1 | tee build/populate_sdk.log`** to capture errors.
- **Obsolete packages** — Ubuntu 24.04 dropped `python3-distutils` and some old libs; skip them (script above does this).

### SSH `Corrupted MAC on input`

Use **WSL SSH** instead, or check board serial console for `sshd` errors.

### `riscv64-unknown-elf-gcc` not found

Ensure apt installed it (step 1) and it's in `PATH`:
```bash
which riscv64-unknown-elf-gcc  # should print /usr/bin/...
```

### Board unreachable (no ping / SSH timeout)

- Board IP is **`192.168.8.100`** by default; check **`AGENT_ENVIRONMENT.md`** for overrides.
- Board and dev machine must be on same subnet (e.g. **`192.168.8.x`**) or SSH forwarded.
- Verify **`sshd`** is running on board (serial console or board manual).

---

## References

- **Yocto Project:** https://docs.yoctoproject.org/
- **PolarFire SoC BSP:** https://github.com/polarfire-soc/meta-polarfire-soc-yocto-bsp
- **Discovery Kit:** https://www.microchip.com/en-us/products/fpgas-and-plds/system-on-chip-fpgas/polarfire-soc-fpgas/
- **This project:** `docs/workflow/WORKFLOW.md`, `AGENT_ENVIRONMENT.md`

---

## Lessons & notes (update after each session)

- ✓ **Windows SSH incompatible** with board SSH (MAC negotiation). Use WSL.
- ✓ **Yocto host packages** — some Ubuntu 24.04 names differ from older docs; script above handles it.
- (Add more as you encounter them.)

