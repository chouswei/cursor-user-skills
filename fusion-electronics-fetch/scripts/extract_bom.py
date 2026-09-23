#!/usr/bin/env python3
"""Extract parts + nets from an Eagle/Fusion Electronics .sch (XML) into bom-extract.json."""

from __future__ import annotations

import argparse
import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

PART_RE = re.compile(r"<part\s+([^>]+?)(?:/>|>(.*?)</part>)", re.I | re.S)
ATTR_RE = re.compile(r'(\w+)="([^"]*)"')
ATTR_CHILD_RE = re.compile(
    r'<(?:attribute|att_value)\s+[^>]*name="([^"]+)"[^>]*value="([^"]*)"',
    re.I,
)
NET_RE = re.compile(r'<net\s+name="([^"]+)"')
SKIP_PREFIXES = ("GND", "FRAME", "SUPPLY")
CORE_COLS = ("name", "value", "deviceset", "device", "package")
VOLTAGE_KEYS = frozenset({"VOLTAGE", "VOLTAGE_RATING", "VRATING", "VOLTAGE-RATING"})
TOLERANCE_KEYS = frozenset({"TOLERANCE", "TOL", "TOLERANCE_RATING"})


def _local(tag: str) -> str:
    return tag.rsplit("}", 1)[-1].lower()


def _pick_vt(attrs: dict[str, str]) -> tuple[str, str]:
    voltage = ""
    tolerance = ""
    for key, val in attrs.items():
        ku = key.upper()
        if ku in VOLTAGE_KEYS and not voltage:
            voltage = val
        elif ku in TOLERANCE_KEYS and not tolerance:
            tolerance = val
    return voltage, tolerance


def _named_attrs(el: ET.Element) -> dict[str, str]:
    out: dict[str, str] = {}
    for child in el:
        if _local(child.tag) not in ("attribute", "att_value"):
            continue
        name = child.attrib.get("name", "")
        if name and "value" in child.attrib:
            out[name] = child.attrib.get("value", "")
    return out


def _device_attr_index(root: ET.Element) -> dict[tuple[str, str, str], dict[str, str]]:
    index: dict[tuple[str, str, str], dict[str, str]] = {}
    for lib in root.iter():
        if _local(lib.tag) != "library":
            continue
        lib_name = lib.attrib.get("name", "")
        for ds in lib.iter():
            if _local(ds.tag) != "deviceset":
                continue
            ds_name = ds.attrib.get("name", "")
            for dev in ds:
                if _local(dev.tag) != "devices":
                    continue
                for device in dev:
                    if _local(device.tag) != "device":
                        continue
                    attrs: dict[str, str] = {}
                    for node in device.iter():
                        if _local(node.tag) not in ("attribute", "att_value"):
                            continue
                        name = node.attrib.get("name", "")
                        if name and "value" in node.attrib:
                            attrs[name] = node.attrib.get("value", "")
                    index[(lib_name, ds_name, device.attrib.get("name", ""))] = attrs
    return index


def _row(
    core: dict[str, str],
    voltage: str,
    tolerance: str,
) -> dict[str, str] | None:
    name = core.get("name", "")
    if not name or any(name.startswith(p) for p in SKIP_PREFIXES):
        return None
    row = {k: core[k] for k in CORE_COLS if core.get(k)}
    if not row:
        return None
    row["voltage_rating"] = voltage
    row["tolerance"] = tolerance
    return row


def parse_sch_et(root: ET.Element) -> tuple[list[dict], list[str]]:
    device_attrs = _device_attr_index(root)
    parts: list[dict] = []
    for el in root.iter():
        if _local(el.tag) != "part":
            continue
        core = {k: el.attrib[k] for k in CORE_COLS if k in el.attrib}
        lib_attrs = device_attrs.get(
            (
                el.attrib.get("library", ""),
                el.attrib.get("deviceset", ""),
                el.attrib.get("device", ""),
            ),
            {},
        )
        part_attrs = _named_attrs(el)
        merged = dict(lib_attrs)
        merged.update(part_attrs)
        voltage, tolerance = _pick_vt(merged)
        row = _row(core, voltage, tolerance)
        if row:
            parts.append(row)
    nets = sorted(
        {
            el.attrib.get("name", "")
            for el in root.iter()
            if _local(el.tag) == "net" and el.attrib.get("name")
        }
    )
    return parts, nets


def parse_sch_regex(text: str) -> tuple[list[dict], list[str]]:
    parts: list[dict] = []
    for m in PART_RE.finditer(text):
        core = dict(ATTR_RE.findall(m.group(1)))
        child_xml = m.group(2) or ""
        child_attrs = dict(ATTR_CHILD_RE.findall(child_xml))
        voltage, tolerance = _pick_vt(child_attrs)
        row = _row(core, voltage, tolerance)
        if row:
            parts.append(row)
    nets = sorted(set(NET_RE.findall(text)))
    return parts, nets


def parse_sch(path: Path) -> dict:
    text = path.read_text(encoding="utf-8", errors="replace")
    try:
        cleaned = re.sub(r"<!DOCTYPE[^>]*>", "", text, count=1, flags=re.I)
        root = ET.fromstring(cleaned)
        parts, nets = parse_sch_et(root)
    except ET.ParseError:
        parts, nets = parse_sch_regex(text)
    return {
        "source": path.name,
        "part_count": len(parts),
        "parts": parts,
        "nets": nets,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("sch", type=Path, help="Path to .sch file")
    ap.add_argument(
        "-o",
        "--output",
        type=Path,
        default=None,
        help="Output JSON (default: <sch-dir>/bom-extract.json)",
    )
    args = ap.parse_args()
    sch: Path = args.sch
    if not sch.is_file():
        print(f"error: not a file: {sch}", file=sys.stderr)
        return 1
    data = parse_sch(sch)
    out = args.output or (sch.parent / "bom-extract.json")
    out.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    print(f"{sch.name}: parts={data['part_count']} nets={len(data['nets'])} -> {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
