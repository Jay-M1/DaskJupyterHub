#!/bin/bash

/usr/sbin/nscd
/usr/sbin/sssd -D

mkdir -p /var/lib/condor 
chown -R condor:condor /var/lib/condor 
chmod -R 755 /var/lib/condor
chmod -R 1777 /var/lib/condor/fs_auth/

condor_master

dask-gateway-server --config /srv/dask-gateway-server-config.py
