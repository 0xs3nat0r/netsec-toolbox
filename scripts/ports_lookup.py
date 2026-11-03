#!/usr/bin/env python3
"""Look up common ports/services from data/ports.csv.

Usage:
    python3 scripts/ports_lookup.py 22
    python3 scripts/ports_lookup.py ssh

TODO: fuzzy search, add --json flag.
"""
import csv
import sys
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "data" / "ports.csv"


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__)
        return 1
    query = sys.argv[1].lower()
    found = False
    with DATA.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if query in (row["port"], row["service"].lower()) or query in row["description"].lower():
                print(f'{row["port"]}/{row["protocol"]}\t{row["service"]}\t{row["description"]}')
                found = True
    if not found:
        print("No match. Add it to data/ports.csv!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
