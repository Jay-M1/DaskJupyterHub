#!/usr/bin/env bash

# Copy requirements to subdirectories
for dir in rocky coffea-backup jupy/notebook; do
    cp requirements.txt $dir/requirements.txt
done

# Copy local dask-gateway-htcondor package into rocky build context
rm -rf rocky/dask-gateway-htcondor/
cp -r /home/jmustafi/dask-gateway-htcondor/dask-gateway-htcondor/ rocky/dask-gateway-htcondor/

# Stop and remove all containers
docker stop $(docker ps -aq) 2>/dev/null
docker rm $(docker ps -aq) 2>/dev/null

# Leave swarm if already in one (reset state)
docker swarm leave --force 2>/dev/null

# Clean up networks and images
docker network prune -f
docker network rm $(docker network ls -q) 2>/dev/null
docker rmi -f $(docker images -q) 2>/dev/null

# Ensure dask-gateway staging directory exists and is writable
mkdir -p ~/.dask-gateway

# Initialize swarm with specific IP (required for overlay networking)
docker swarm init --advertise-addr 129.13.101.141

# Build and start services
docker compose build
docker compose up -d
docker ps
