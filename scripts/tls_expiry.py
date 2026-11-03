#!/usr/bin/env python3
"""Check how many days remain before a server's TLS certificate expires.

Usage:
    python3 scripts/tls_expiry.py HOST[:PORT] [HOST[:PORT] ...] [--warn 14]

Example:
    python3 scripts/tls_expiry.py example.com github.com:443

Exit code is 1 if any certificate expires within --warn days or cannot be checked.

TODO: STARTTLS (SMTP/IMAP), print issuer and SANs, JSON output.
"""
import argparse
import socket
import ssl
import sys
import time


def days_left(host: str, port: int, timeout: float = 5.0) -> float:
    ctx = ssl.create_default_context()
    with socket.create_connection((host, port), timeout=timeout) as sock:
        with ctx.wrap_socket(sock, server_hostname=host) as tls:
            cert = tls.getpeercert()
    expires = ssl.cert_time_to_seconds(cert["notAfter"])
    return (expires - time.time()) / 86400


def split_target(target: str) -> tuple[str, int]:
    host, _, port = target.partition(":")
    return host, int(port) if port else 443


def main() -> int:
    parser = argparse.ArgumentParser(description="TLS certificate expiry checker")
    parser.add_argument("targets", nargs="+")
    parser.add_argument("--warn", type=float, default=14, help="warn below this many days")
    args = parser.parse_args()

    status = 0
    for target in args.targets:
        host, port = split_target(target)
        try:
            days = days_left(host, port)
        except (OSError, ssl.SSLError) as exc:
            print(f"{target}\tERROR\t{exc}")
            status = 1
            continue
        flag = "WARN" if days < args.warn else "ok"
        if days < args.warn:
            status = 1
        print(f"{target}\t{flag}\t{days:.1f} days left")
    return status


if __name__ == "__main__":
    sys.exit(main())
