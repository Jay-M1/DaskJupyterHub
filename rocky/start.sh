#!/bin/sh
echo ">>> in start.sh"

condor_master

echo ">>> executed condor_master"

dask-gateway-server

echo ">>> Executed dask-gateway-server --config /work/dask-gateway_server_config.py"
