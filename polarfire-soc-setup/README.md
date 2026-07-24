# polarfire-soc-setup

Set up a **PolarFire SoC Discovery Kit** embedded firmware project with **WSL cross-compilation**, **Yocto SDK**, and **board SSH access**.

## Quick start

### Local (project `.cursor/skills/`)

This skill is already in `.cursor/skills/polarfire-soc-setup/`. Use it with Cursor AI:

- Open **SKILL.md** in your editor.
- Follow the **5-step quick setup** (WSL deps → Yocto sync → SDK build → SSH).

### Install across projects (via skillfish)

```bash
npx skillfish add YOUR_ORG/polarfire-soc-setup
```

Then access from any Cursor workspace:

```
~/.cursor/skills/polarfire-soc-setup/SKILL.md
```

## What's included

- **SKILL.md** — Full setup guide (5 steps, troubleshooting, references)
- **references.md** — Links to Yocto, PolarFire BSP, board docs
- **skillfish.json** — Portable skill manifest (installable via `npx skillfish`)

## Prerequisites

- **Windows 10/11** with **WSL2 + Ubuntu 24.04**
- **~50 GB free disk** in WSL (for Yocto build)
- **Network** to GitHub (repo, BSP manifests)

## Steps (summary)

1. Install WSL build dependencies (`apt-get`)
2. Sync PolarFire Yocto 2025.03 (`repo init / repo sync`)
3. Configure BSP for Discovery Kit (`source setup.sh -m mpfs-disco-kit`)
4. Build SDK (`bitbake … -c populate_sdk`) — **2–4 hours**
5. Install SDK to `/opt` (`finish_yocto_sdk_install.sh`)

**Then:** Source the environment script before each build and deploy to board via WSL SSH.

## SSH troubleshooting

- **Linux / WSL** ✓ — Works out of the box
- **Windows OpenSSH** ✗ — MAC negotiation issue; use workaround in SKILL.md

## Publishing this skill

To share with a team or the community:

```bash
# Create a GitHub repo
git init polarfire-soc-setup
git add .
git commit -m "Initial: PolarFire SoC setup skill"
git branch -M main
git remote add origin https://github.com/YOUR_ORG/polarfire-soc-setup.git
git push -u origin main

# Register on skill.fish
npx skillfish submit
```

## License

MIT

## References

- **Yocto Project** — https://docs.yoctoproject.org/
- **PolarFire SoC BSP** — https://github.com/polarfire-soc/meta-polarfire-soc-yocto-bsp
- **Discovery Kit** — https://www.microchip.com/en-us/products/fpgas-and-plds/system-on-chip-fpgas/polarfire-soc-fpgas/
- **skillfish CLI** — https://skill.fish/

