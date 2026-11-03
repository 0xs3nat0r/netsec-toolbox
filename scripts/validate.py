#!/usr/bin/env python3
"""Validate repo content: CSV structure and cheatsheet format.

Usage:
    python3 scripts/validate.py
"""
import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
errors: list[str] = []


def validate_ports() -> None:
    path = ROOT / "data" / "ports.csv"
    expected = ["port", "protocol", "service", "description"]
    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames != expected:
            errors.append(f"{path.name}: header must be {expected}")
            return
        seen = set()
        for n, row in enumerate(reader, start=2):
            if not row["port"].isdigit() or not 0 < int(row["port"]) < 65536:
                errors.append(f"{path.name}:{n}: invalid port {row['port']!r}")
            if row["protocol"] not in {"tcp", "udp", "both"}:
                errors.append(f"{path.name}:{n}: protocol must be tcp/udp/both")
            key = (row["port"], row["protocol"], row["service"])
            if key in seen:
                errors.append(f"{path.name}:{n}: duplicate row {key}")
            seen.add(key)


def validate_cheatsheets() -> None:
    for path in sorted((ROOT / "cheatsheets").glob("*.md")):
        text = path.read_text(encoding="utf-8")
        if not text.lstrip().startswith("# "):
            errors.append(f"{path.name}: must start with a '# Title' heading")
        if text.count("```") % 2:
            errors.append(f"{path.name}: unclosed code block")


def main() -> int:
    validate_ports()
    validate_cheatsheets()
    for e in errors:
        print("ERROR:", e)
    print("OK" if not errors else f"{len(errors)} problem(s) found")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
