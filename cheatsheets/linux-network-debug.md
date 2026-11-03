# Linux network debugging

## Interfaces, IPs, routes
```bash
ip -br a
ip route
```

## Listening sockets and owning processes
```bash
sudo ss -tulpn
```

## Who is connected to a port
```bash
ss -tn state established '( sport = :443 )'
```

## DNS lookups
```bash
dig example.com +short
dig @1.1.1.1 example.com A
```

## Trace route / path quality
```bash
mtr -rwzc 50 example.com
```

## Quick firewall view (iptables / nftables)
```bash
sudo iptables -L -n -v
sudo nft list ruleset
```

## Test a TCP port without extra tools
```bash
timeout 3 bash -c '</dev/tcp/example.com/443' && echo open || echo closed
```

TODO: conntrack, tc (traffic shaping), MTU debugging, IPv6 equivalents.
