#!/usr/bin/env python3
"""Validate repo content: CSV structure and cheatsheet format.

Usage:
    python3 scripts/validate.py
"""
import csv
import ipaddress
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
errors: list[str] = []


def load(name: str, expected: list[str]):
    """Return CSV rows if the header matches, else record an error and return None."""
    path = DATA / name
    if not path.exists():
        errors.append(f"{name}: file is missing")
        return None
    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames != expected:
            errors.append(f"{name}: header must be {expected}")
            return None
        rows = list(reader)
    for n, row in enumerate(rows, start=2):
        if None in row or any(v is None or v == "" for v in row.values()):
            errors.append(f"{name}:{n}: wrong number of columns or empty value")
            return None
    return rows


def check_unique(name: str, rows, key_fn) -> None:
    seen = set()
    for n, row in enumerate(rows, start=2):
        key = key_fn(row)
        if key in seen:
            errors.append(f"{name}:{n}: duplicate row {key}")
        seen.add(key)


def validate_ports() -> None:
    rows = load("ports.csv", ["port", "protocol", "service", "description"])
    if rows is None:
        return
    for n, row in enumerate(rows, start=2):
        if not row["port"].isdigit() or not 0 < int(row["port"]) < 65536:
            errors.append(f"ports.csv:{n}: invalid port {row['port']!r}")
        if row["protocol"] not in {"tcp", "udp", "both"}:
            errors.append(f"ports.csv:{n}: protocol must be tcp/udp/both")
    check_unique("ports.csv", rows, lambda r: (r["port"], r["protocol"], r["service"]))


def validate_http_status() -> None:
    rows = load("http_status.csv", ["code", "name", "category", "description"])
    if rows is None:
        return
    categories = {"success", "redirect", "client error", "server error", "informational"}
    for n, row in enumerate(rows, start=2):
        if not (row["code"].isdigit() and 100 <= int(row["code"]) <= 599):
            errors.append(f"http_status.csv:{n}: invalid status code {row['code']!r}")
        if row["category"] not in categories:
            errors.append(f"http_status.csv:{n}: category must be one of {sorted(categories)}")
    check_unique("http_status.csv", rows, lambda r: r["code"])


def validate_ip_ranges() -> None:
    rows = load("ip_ranges.csv", ["cidr", "name", "rfc", "description"])
    if rows is None:
        return
    for n, row in enumerate(rows, start=2):
        try:
            ipaddress.ip_network(row["cidr"])
        except ValueError:
            errors.append(f"ip_ranges.csv:{n}: invalid CIDR {row['cidr']!r}")
    check_unique("ip_ranges.csv", rows, lambda r: r["cidr"])


def validate_icmp() -> None:
    rows = load("icmp_types.csv", ["type", "code", "name", "description"])
    if rows is None:
        return
    for n, row in enumerate(rows, start=2):
        for field in ("type", "code"):
            if not (row[field].isdigit() and 0 <= int(row[field]) <= 255):
                errors.append(f"icmp_types.csv:{n}: {field} must be 0-255")
    check_unique("icmp_types.csv", rows, lambda r: (r["type"], r["code"]))


def validate_tcp_flags() -> None:
    rows = load("tcp_flags.csv", ["flag", "name", "bit", "description"])
    if rows is None:
        return
    for n, row in enumerate(rows, start=2):
        try:
            value = int(row["bit"], 16)
        except ValueError:
            errors.append(f"tcp_flags.csv:{n}: bit must be hex like 0x02")
            continue
        if value not in {1 << i for i in range(8)}:
            errors.append(f"tcp_flags.csv:{n}: bit must be a single-bit value")
    check_unique("tcp_flags.csv", rows, lambda r: r["flag"])


def validate_cheatsheets() -> None:
    for path in sorted((ROOT / "cheatsheets").glob("*.md")):
        text = path.read_text(encoding="utf-8")
        if not text.lstrip().startswith("# "):
            errors.append(f"{path.name}: must start with a '# Title' heading")
        if text.count("```") % 2:
            errors.append(f"{path.name}: unclosed code block")


def main() -> int:
    validate_ports()
    validate_http_status()
    validate_ip_ranges()
    validate_icmp()
    validate_tcp_flags()
    validate_cheatsheets()
    for e in errors:
        print("ERROR:", e)
    print("OK" if not errors else f"{len(errors)} problem(s) found")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
