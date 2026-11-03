#!/usr/bin/env python3
"""Measure DNS response time of a resolver using raw UDP queries (stdlib only).

Usage:
    python3 scripts/dns_timing.py example.com --resolver 1.1.1.1 --count 5

TODO: AAAA/MX/TXT query types, TCP fallback, compare multiple resolvers in one run.
"""
import argparse
import random
import socket
import struct
import time


def build_query(name: str) -> bytes:
    """Build a standard recursive A-record query."""
    header = struct.pack(">HHHHHH", random.randrange(65536), 0x0100, 1, 0, 0, 0)
    qname = b"".join(bytes([len(p)]) + p.encode("ascii") for p in name.rstrip(".").split("."))
    return header + qname + b"\x00" + struct.pack(">HH", 1, 1)  # type A, class IN


def parse_response(data: bytes) -> tuple[int, int]:
    """Return (rcode, answer_count) from a DNS response."""
    _, flags, _, answers, _, _ = struct.unpack(">HHHHHH", data[:12])
    return flags & 0x000F, answers


def query_once(name: str, resolver: str, timeout: float) -> tuple[float, int, int]:
    packet = build_query(name)
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.settimeout(timeout)
        start = time.perf_counter()
        sock.sendto(packet, (resolver, 53))
        data, _ = sock.recvfrom(4096)
        elapsed = (time.perf_counter() - start) * 1000
    rcode, answers = parse_response(data)
    return elapsed, rcode, answers


def main() -> None:
    parser = argparse.ArgumentParser(description="DNS response time")
    parser.add_argument("name")
    parser.add_argument("--resolver", default="1.1.1.1")
    parser.add_argument("--count", type=int, default=5)
    parser.add_argument("--timeout", type=float, default=2.0)
    args = parser.parse_args()

    times = []
    for i in range(1, args.count + 1):
        try:
            ms, rcode, answers = query_once(args.name, args.resolver, args.timeout)
        except OSError as exc:
            print(f"#{i}: error: {exc}")
            continue
        times.append(ms)
        print(f"#{i}: {ms:.1f} ms  rcode={rcode} answers={answers}")
    if times:
        print(f"min/avg/max = {min(times):.1f}/{sum(times)/len(times):.1f}/{max(times):.1f} ms")


if __name__ == "__main__":
    main()
