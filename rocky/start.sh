#!/bin/sh
condor_master
dask-gateway-server --config dask-gateway_server_config.py
