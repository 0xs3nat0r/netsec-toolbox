# tcpdump

## Capture on an interface, no name resolution
```bash
sudo tcpdump -i eth0 -nn
```

## Filter by host and port
```bash
sudo tcpdump -i eth0 -nn host 10.0.0.5 and port 443
```

## Only DNS traffic
```bash
sudo tcpdump -i any -nn port 53
```

## Save to file / read from file
```bash
sudo tcpdump -i eth0 -w capture.pcap
tcpdump -nn -r capture.pcap
```

## Show packet contents (ASCII)
```bash
sudo tcpdump -i eth0 -A -s0 port 80
```

TODO: TCP flag filters (SYN/RST), rotating capture files, BPF cheatsheet.
TODO: Test14