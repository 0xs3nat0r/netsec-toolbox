#!/usr/bin/env python3
"""Print details about an IPv4/IPv6 network or address in CIDR.

Usage:
    python3 scripts/cidr_info.py 192.168.1.0/24
    python3 scripts/cidr_info.py 10.1.2.3/20
    python3 scripts/cidr_info.py 2001:db8::/48

TODO: subnet splitting (--split 26), supernet aggregation, list overlapping ranges.
"""
import ipaddress
import sys


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__)
        return 1
    try:
        net = ipaddress.ip_network(sys.argv[1], strict=False)
    except ValueError as exc:
        print(f"Invalid network: {exc}")
        return 1

    print(f"Network:        {net}")
    print(f"Version:        IPv{net.version}")
    print(f"Netmask:        {net.netmask}")
    print(f"Prefix length:  /{net.prefixlen}")
    print(f"Addresses:      {net.num_addresses}")
    if net.version == 4:
        print(f"Hostmask:       {net.hostmask}")
        print(f"Broadcast:      {net.broadcast_address}")
    hosts_first = net.network_address + (1 if net.version == 4 and net.prefixlen < 31 else 0)
    hosts_last = net.broadcast_address - (1 if net.version == 4 and net.prefixlen < 31 else 0)
    print(f"First usable:   {hosts_first}")
    print(f"Last usable:    {hosts_last}")
    print(f"Private:        {net.is_private}")
    print(f"Global:         {net.is_global}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
