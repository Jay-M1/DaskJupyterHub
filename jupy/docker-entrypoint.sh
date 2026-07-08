#!/bin/bash
set -e

mkdir -p /var/lib/sss/db /var/lib/sss/pipes /var/log/sssd
sssd -D

exec "$@"
