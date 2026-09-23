#!/usr/bin/env python3
"""Minimal tests for extract_bom VOLTAGE/TOLERANCE retention."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from extract_bom import parse_sch

SAMPLE = """<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE eagle SYSTEM "eagle.dtd">
<eagle version="9.7.0">
<drawing>
<schematic>
<libraries>
<library name="rcl">
<devicesets>
<deviceset name="C-EU">
<devices>
<device name="C0603" package="C0603">
<attribute name="VOLTAGE" value="50V"/>
<attribute name="TOLERANCE" value="10%"/>
</device>
</devices>
</deviceset>
<deviceset name="R-EU_">
<devices>
<device name="R0603" package="R0603"/>
</devices>
</deviceset>
</devicesets>
</library>
<library name="conn">
<devicesets>
<deviceset name="J1">
<devices>
<device name="">
<att_values>
<att_value name="VOLTAGE" value="400V"/>
</att_values>
</device>
</devices>
</deviceset>
</devicesets>
</library>
</libraries>
<parts>
<part name="C1" library="rcl" deviceset="C-EU" device="C0603" value="100n"/>
<part name="C2" library="rcl" deviceset="C-EU" device="C0603" value="10n">
<attribute name="VOLTAGE" value="25V"/>
</part>
<part name="R1" library="rcl" deviceset="R-EU_" device="R0603" value="10k">
<attribute name="TOLERANCE" value="1%"/>
</part>
<part name="J9" library="conn" deviceset="J1" device=""/>
<part name="GND1" library="supply1" deviceset="GND" device=""/>
</parts>
<nets>
<net name="N$1"/>
</nets>
</schematic>
</drawing>
</eagle>
"""


class ExtractBomVoltageTolerance(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.NamedTemporaryFile(
            suffix=".sch", delete=False, mode="w", encoding="utf-8"
        )
        self._tmp.write(SAMPLE)
        self._tmp.close()
        self.path = Path(self._tmp.name)

    def tearDown(self) -> None:
        self.path.unlink(missing_ok=True)

    def test_maps_voltage_and_tolerance(self) -> None:
        data = parse_sch(self.path)
        by_name = {p["name"]: p for p in data["parts"]}
        self.assertNotIn("GND1", by_name)
        self.assertEqual(by_name["C1"]["voltage_rating"], "50V")
        self.assertEqual(by_name["C1"]["tolerance"], "10%")
        self.assertEqual(by_name["C2"]["voltage_rating"], "25V")
        self.assertEqual(by_name["C2"]["tolerance"], "10%")
        self.assertEqual(by_name["R1"]["voltage_rating"], "")
        self.assertEqual(by_name["R1"]["tolerance"], "1%")
        self.assertEqual(by_name["J9"]["voltage_rating"], "400V")
        self.assertEqual(by_name["J9"]["tolerance"], "")
        self.assertEqual(data["part_count"], 4)


if __name__ == "__main__":
    unittest.main()
