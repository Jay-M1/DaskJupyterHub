#!/bin/sh
/usr/sbin/condor_master -f
dask-gateway-server --config dask-gateway_server_config.py