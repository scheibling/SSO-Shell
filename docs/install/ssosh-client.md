# SSO Shell Client
## Installation
```bash
./ssosh-client install
```

## Usage
```bash
# Login to server (retrieve single-use certificate if allowed on principal)
ssosh SERVER01

# Get certificate manually
ssosh certificate get --key .ssh/id_ecdsa

# List certificates
ssosh certificate list

# Get certificate information
ssosh certificate info --certificate .ssh/id_ecdsa-cert.pub

# Get certificate principals
ssosh certificate info --certificate .ssh/id_ecdsa-cert.pub --get-principals

# Validate certificate expiration
ssosh certificate validate --certificate .ssh/id_ecdsa-cert.pub
```