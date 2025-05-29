#!/bin/bash

/usr/sbin/nscd
/usr/sbin/sssd -D

condor_master

dask-gateway-server --config /work/dask-gateway_server_config.py
