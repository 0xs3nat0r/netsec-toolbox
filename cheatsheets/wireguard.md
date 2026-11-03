# WireGuard

## Generate a key pair
```bash
umask 077
wg genkey | tee private.key | wg pubkey > public.key
```

## Server config (/etc/wireguard/wg0.conf)
```ini
[Interface]
Address = 10.8.0.1/24
ListenPort = 51820
PrivateKey = <server-private-key>

[Peer]
PublicKey = <client-public-key>
AllowedIPs = 10.8.0.2/32
```

## Client config
```ini
[Interface]
Address = 10.8.0.2/24
PrivateKey = <client-private-key>
DNS = 1.1.1.1

[Peer]
PublicKey = <server-public-key>
Endpoint = server.example.com:51820
AllowedIPs = 0.0.0.0/0, ::/0
PersistentKeepalive = 25
```

## Bring interface up/down, enable at boot
```bash
sudo wg-quick up wg0
sudo wg-quick down wg0
sudo systemctl enable --now wg-quick@wg0
```

## Show status
```bash
sudo wg show
```

## Enable IP forwarding on the server
```bash
echo 'net.ipv4.ip_forward=1' | sudo tee /etc/sysctl.d/99-wg.conf
sudo sysctl --system
```

TODO: NAT rules for full-tunnel clients, preshared keys, multiple peers script.
