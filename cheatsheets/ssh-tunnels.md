# SSH tunnels & tricks

## Local port forward (access remote service locally)
```bash
ssh -L 8080:localhost:80 user@server
```

## Remote port forward (expose a local service on the server)
```bash
ssh -R 9000:localhost:3000 user@server
```

## Dynamic SOCKS5 proxy
```bash
ssh -D 1080 -N user@server
```

## Jump host
```bash
ssh -J user@bastion user@internal-host
```

## Keep connection alive (~/.ssh/config)
```
Host *
    ServerAliveInterval 30
    ServerAliveCountMax 3
```

## Generate a modern key
```bash
ssh-keygen -t ed25519 -C "comment"
```

TODO: autossh for persistent tunnels, systemd unit example, hardening sshd_config.
