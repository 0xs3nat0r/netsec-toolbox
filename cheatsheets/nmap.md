# Nmap

> Scan only hosts you own or are authorized to test.

## Quick host discovery (ping sweep)
```bash
nmap -sn 192.168.1.0/24
```

## Fast scan of top ports
```bash
nmap -F target
```

## Full TCP port scan + service versions
```bash
nmap -p- -sV -T4 target
```

## Default scripts + version + OS (needs root)
```bash
sudo nmap -sC -sV -O target
```

## Save output in all formats
```bash
nmap -oA scan_result target
```

TODO: UDP scanning, NSE script categories, timing/evasion notes for IDS testing in labs.
