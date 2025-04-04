docker network prune -f
docker stop $(docker ps -aq)
docker rm $(docker ps -aq)
docker network rm $(docker network ls -q)
docker rmi -f $(docker images -q)

docker compose build
docker compose up -d
