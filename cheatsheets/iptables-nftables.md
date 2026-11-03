# iptables / nftables

> Test firewall changes with console access or a rollback timer, so you don't lock yourself out of a remote server.

## List rules with counters
```bash
sudo iptables -L -n -v --line-numbers
sudo nft list ruleset
```

## Basic iptables server policy
```bash
sudo iptables -A INPUT -i lo -j ACCEPT
sudo iptables -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 22 -j ACCEPT
sudo iptables -P INPUT DROP
```

## Delete a rule by number
```bash
sudo iptables -D INPUT 3
```

## Rate-limit new SSH connections
```bash
sudo iptables -A INPUT -p tcp --dport 22 -m conntrack --ctstate NEW -m limit --limit 6/min --limit-burst 6 -j ACCEPT
```

## Minimal nftables ruleset (/etc/nftables.conf)
```
table inet filter {
  chain input {
    type filter hook input priority 0; policy drop;
    iif lo accept
    ct state established,related accept
    tcp dport 22 accept
  }
}
```

## Apply / persist
```bash
sudo nft -f /etc/nftables.conf
sudo systemctl enable --now nftables
```

TODO: NAT/masquerade, port forwarding, logging dropped packets, ipset/nft sets.
