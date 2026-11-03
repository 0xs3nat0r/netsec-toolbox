# Wireshark filters

## Display filters (applied after capture)

### By host / port
```
ip.addr == 10.0.0.5
tcp.port == 443
ip.src == 10.0.0.5 && tcp.dstport == 80
```

### Protocol
```
dns
http.request
tls.handshake.type == 1
```

### TCP problems
```
tcp.analysis.retransmission
tcp.flags.reset == 1
tcp.analysis.zero_window
```

### SYNs without ACK (connection attempts)
```
tcp.flags.syn == 1 && tcp.flags.ack == 0
```

### DNS queries for a name
```
dns.qry.name contains "example.com"
```

### TLS SNI (server name)
```
tls.handshake.extensions_server_name == "example.com"
```

## Capture filters (BPF, applied while capturing)
```
host 10.0.0.5 and port 443
not port 22
net 192.168.1.0/24
```

TODO: following streams, exporting objects, decrypting TLS with SSLKEYLOGFILE in lab setups, tshark one-liners.
