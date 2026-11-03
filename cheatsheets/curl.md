# curl

## Headers only
```bash
curl -I https://example.com
```

## Verbose (shows TLS handshake and headers)
```bash
curl -v https://example.com
```

## Follow redirects
```bash
curl -L https://example.com
```

## Timing breakdown
```bash
curl -o /dev/null -s -w 'dns=%{time_namelookup} connect=%{time_connect} tls=%{time_appconnect} ttfb=%{time_starttransfer} total=%{time_total}\n' https://example.com
```

## Test a server by IP with a specific hostname
```bash
curl --resolve example.com:443:203.0.113.10 https://example.com
```

## Send JSON
```bash
curl -X POST https://api.example.com/items -H 'Content-Type: application/json' -d '{"name":"test"}'
```

## Use a SOCKS5 proxy (DNS resolved by the proxy)
```bash
curl --socks5-hostname 127.0.0.1:1080 https://example.com
```

## Set timeouts
```bash
curl --connect-timeout 5 --max-time 20 https://example.com
```

TODO: client certificates, retries, cookies, HTTP/3 (`--http3`), `-k` caveats.
