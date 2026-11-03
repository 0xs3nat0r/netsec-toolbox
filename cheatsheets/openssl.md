# OpenSSL

## Inspect a server's certificate
```bash
openssl s_client -connect example.com:443 -servername example.com </dev/null 2>/dev/null | openssl x509 -noout -subject -issuer -dates
```

## Show full certificate chain
```bash
openssl s_client -connect example.com:443 -servername example.com -showcerts </dev/null
```

## Will a certificate expire within 30 days? (exit code 1 if yes)
```bash
openssl x509 -in cert.pem -noout -checkend $((30*86400))
```

## Generate a private key and self-signed certificate (lab use)
```bash
openssl req -x509 -newkey rsa:3072 -nodes -keyout key.pem -out cert.pem -days 365 -subj "/CN=localhost"
```

## Create a CSR from an existing key
```bash
openssl req -new -key key.pem -out request.csr -subj "/CN=example.com"
```

## Verify a certificate against a CA bundle
```bash
openssl verify -CAfile ca-bundle.pem cert.pem
```

## Check which TLS version a server accepts
```bash
openssl s_client -connect example.com:443 -tls1_2 </dev/null
openssl s_client -connect example.com:443 -tls1_3 </dev/null
```

## File hashes
```bash
openssl dgst -sha256 file.bin
```

TODO: PKCS#12 conversion, OCSP stapling check, cipher suite listing.
