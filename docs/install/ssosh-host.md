# SSO Shell Host
# Installation
## Provision host and install daemon
```bash
$ ./ssosh-host provision
Enter the URL
  https://ssosh.io
Enter the hostname (default: HOSTNAME)
  HOSTNAME
Enter the provisioning secret
  SECRET
At what interval should the daemon refresh the SSH CA Certificate (default: 1h)
  1h
At what interval should the daemon refresh the principal list (default: 10m)
  10m

Finished!
```

## Start, stop, restart
```bash
systemctl start ssosh-host
systemctl stop ssosh-host
systemctl restart ssosh-host
```