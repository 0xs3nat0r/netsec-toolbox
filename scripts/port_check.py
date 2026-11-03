#!/usr/bin/env python3
"""Simple concurrent TCP port checker (starter version).

Usage:
    python3 scripts/port_check.py HOST PORT [PORT ...] [--timeout 2]

Example:
    python3 scripts/port_check.py example.com 80 443

Only use on hosts you own or are authorized to test.

TODO: port ranges (1-1024), JSON output, IPv6 handling, banner grabbing (opt-in).
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


def main() -> None:
    parser = argparse.ArgumentParser(description="Check if TCP ports are open")
    parser.add_argument("host")
    parser.add_argument("ports", type=int, nargs="+")
    parser.add_argument("--timeout", type=float, default=2.0)
    args = parser.parse_args()

    with ThreadPoolExecutor(max_workers=min(32, len(args.ports))) as pool:
        results = pool.map(lambda p: check(args.host, p, args.timeout), args.ports)
        for port, is_open in sorted(results):
            print(f"{args.host}:{port}\t{'open' if is_open else 'closed/filtered'}")


if __name__ == "__main__":
    main()
