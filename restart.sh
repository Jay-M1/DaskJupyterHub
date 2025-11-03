#!/usr/bin/env bash

for dir in rocky coffea-backup jupy/notebook; do
    cp requirements.txt $dir/requirements.txt
done

docker network prune -f
docker stop $(docker ps -aq)
docker rm $(docker ps -aq)
docker network rm $(docker network ls -q)
docker rmi -f $(docker images -q)

docker compose build
docker compose up -d
docker ps
