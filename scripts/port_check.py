#!/usr/bin/env python3
"""Simple concurrent TCP port checker (starter version).

Usage:
    python3 scripts/port_check.py HOST PORT_OR_RANGE [...] [--timeout 2] [--open-only]

Examples:
    python3 scripts/port_check.py example.com 80 443
    python3 scripts/port_check.py 192.168.1.10 20-25 8000-8100 --open-only

Only use on hosts you own or are authorized to test.

TODO: JSON output, IPv6 handling, banner grabbing (opt-in).
"""
import argparse
import socket
from concurrent.futures import ThreadPoolExecutor


def check(host: str, port: int, timeout: float) -> tuple[int, bool]:
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return port, True
    except OSError:
        return port, False


def parse_ports(items: list[str]) -> list[int]:
    ports: set[int] = set()
    for item in items:
        start, _, end = item.partition("-")
        lo, hi = int(start), int(end or start)
        if not (0 < lo <= hi < 65536):
            raise ValueError(f"invalid port or range: {item!r}")
        ports.update(range(lo, hi + 1))
    return sorted(ports)


def main() -> None:
    parser = argparse.ArgumentParser(description="Check if TCP ports are open")
    parser.add_argument("host")
    parser.add_argument("ports", nargs="+", help="ports or ranges, e.g. 80 443 1-1024")
    parser.add_argument("--timeout", type=float, default=2.0)
    parser.add_argument("--open-only", action="store_true", help="print only open ports")
    args = parser.parse_args()

    try:
        ports = parse_ports(args.ports)
    except ValueError as exc:
        parser.error(str(exc))

    with ThreadPoolExecutor(max_workers=min(64, len(ports))) as pool:
        results = pool.map(lambda p: check(args.host, p, args.timeout), ports)
        for port, is_open in results:
            if is_open or not args.open_only:
                print(f"{args.host}:{port}\t{'open' if is_open else 'closed/filtered'}")


if __name__ == "__main__":
    main()
