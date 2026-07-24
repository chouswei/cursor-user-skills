# PC UI type playbook

## Basement goal

Desktop-shell hello window (toolkit chosen by user).

## Ask (if unknown)

- Toolkit: Tauri, Qt, WPF, Flutter desktop, other
- Must ship offline?

## Create

- Toolkit-minimal project under `desktop/` (hybrid) or repo root (single)
- One window / hello label
- README — install deps, run debug build

## vs html-ui

- `pc-ui` = installable/native shell
- `html-ui` = browser. If both: hybrid `pc-ui + html-ui` (e.g. Tauri + web assets) with explicit ownership of UI folder
