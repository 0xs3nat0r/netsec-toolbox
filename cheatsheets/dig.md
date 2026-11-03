# dig (DNS)

## Short answer
```bash
dig example.com +short
```

## Specific record types
```bash
dig example.com MX +short
dig example.com TXT +short
dig example.com NS +short
dig example.com AAAA +short
```

## Query a specific resolver
```bash
dig @1.1.1.1 example.com A
```

## Reverse lookup
```bash
dig -x 8.8.8.8 +short
```

## Trace delegation from the root
```bash
dig example.com +trace
```

## Check DNSSEC records
```bash
dig example.com DNSKEY +dnssec +short
```

## Check SPF / DMARC
```bash
dig example.com TXT +short | grep spf
dig _dmarc.example.com TXT +short
```

## Compare answers from several resolvers
```bash
for r in 1.1.1.1 8.8.8.8 9.9.9.9; do echo "== $r"; dig @$r example.com +short; done
```

TODO: DoT/DoH testing with `kdig`, zone transfer check on your own zones, EDNS options.
