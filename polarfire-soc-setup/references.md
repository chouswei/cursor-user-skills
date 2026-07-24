# References

## Yocto / BitBake

- **Yocto Project Manual** — https://docs.yoctoproject.org/ref-manual/system-requirements.html
- **BitBake populate_sdk** — Generates cross-compilation SDK from Yocto recipes; sources `environment-setup-*` to set `$CC`, `$CFLAGS`, sysroot.

## PolarFire SoC

- **Meta BSP** — https://github.com/polarfire-soc/meta-polarfire-soc-yocto-bsp (v2025.03 current)
- **Manifests** — https://github.com/polarfire-soc/polarfire-soc-yocto-manifests (repo init target)
- **Discovery Kit Reference Design** — https://github.com/polarfire-soc/polarfire-soc-discovery-kit-reference-design

## Board SSH

- **OpenSSH 9.6** running on board (typical PolarFire Linux image).
- **Windows OpenSSH 9.5** has MAC negotiation issue (use WSL SSH as workaround).
- **eth0** or DHCP usually assigns **`192.168.8.100`** by default (check board docs).

## WSL & Linux

- **WSL2 Ubuntu 24.04** — Baseline for cross-compile host.
- **RISC-V GCC** — `riscv64-unknown-elf-gcc` from Ubuntu repositories (13.x series).
- **CMake + Ninja** — Standard Yocto build helpers.

