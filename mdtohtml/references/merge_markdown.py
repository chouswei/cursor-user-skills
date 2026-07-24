#!/usr/bin/env python3
"""
Merge multiple Markdown files into one with UTF-8 encoding preservation.

Python's explicit UTF-8 handling eliminates encoding corruption issues
that occur with PowerShell. Unicode characters (–, →, ↔, etc.) are
preserved intact through proper file I/O encoding.

USAGE:
    python merge_markdown.py <output.md> <input1.md> [input2.md ...]

EXAMPLE (leo-cubesat-laser-comm system design report):
    python merge_markdown.py leo-laser-comm-PAT-system-design-merged.md \
        01-abstract-introduction.md \
        02-architecture.md \
        02b-interconnection.md \
        02b1-mcu-pinmap.md \
        02b2-inter-hat-bridges.md \
        02b3-software-allocation.md \
        02b4-connector-inventory.md \
        03-software-allocation.md \
        04-state-machine.md \
        05-tracking.md \
        06-calibration.md \
        07-storage.md \
        08-faults.md \
        09-device-thread-states.md \
        10-optics.md \
        11-power.md \
        12-references.md

WHY PYTHON?
- Explicit UTF-8 encoding eliminates PowerShell encoding corruption
- Unicode characters (–, →, ↔, etc.) preserved through entire pipeline
- Simpler than sanitizing: read UTF-8 → merge → write UTF-8
- Cross-platform (Windows, macOS, Linux)
"""

import sys
import argparse
from pathlib import Path
from typing import List

# Force UTF-8 output on Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')


def merge_files(input_files: List[Path], output_file: Path) -> None:
    """
    Merge multiple Markdown files into one with explicit UTF-8 encoding.
    
    Unicode characters (–, →, ↔, etc.) are preserved intact through proper
    UTF-8 encoding handling. No sanitization or character replacement needed.
    
    Args:
        input_files: List of Path objects to merge (in order)
        output_file: Path to output merged file
    """
    merged_content = []
    
    for input_file in input_files:
        if not input_file.exists():
            print(f"⚠ Skipped (not found): {input_file.name}")
            continue
        
        try:
            # Read with explicit UTF-8 encoding (preserves all Unicode)
            with open(input_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            merged_content.append(content)
            print(f"✓ Merged: {input_file.name}")
        except UnicodeDecodeError as e:
            print(f"✗ Error reading {input_file.name}: {e}")
            sys.exit(1)
    
    # Join with double newline separator
    final_content = '\n\n'.join(merged_content)
    
    # Write with explicit UTF-8 encoding
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(final_content)
        print(f"\n✓ Successfully merged into: {output_file}")
        print(f"  Total content size: {len(final_content)} bytes")
    except IOError as e:
        print(f"✗ Error writing to {output_file}: {e}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description='Merge Markdown files with UTF-8 encoding preservation'
    )
    parser.add_argument('output', help='Output merged file path')
    parser.add_argument('inputs', nargs='+', help='Input Markdown files to merge')
    
    args = parser.parse_args()
    
    input_files = [Path(f) for f in args.inputs]
    output_file = Path(args.output)
    
    merge_files(input_files, output_file)


if __name__ == '__main__':
    main()
