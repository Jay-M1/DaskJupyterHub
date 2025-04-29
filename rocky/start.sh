#!/bin/sh
echo ">>> in start.sh"

condor_master

usermod -aG input condor

condor_reconfig

echo ">>> executed condor_master"

dask-gateway-server --config /work/dask-gateway_server_config.py

echo ">>> Cluster stopped"
