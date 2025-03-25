docker network prune -f
docker stop $(docker ps -aq)
docker rm $(docker ps -aq)
docker network rm $(docker network ls -q)

docker compose build
docker compose up -d

# docker exec -it my_jupyterhub-htrocky-1 /bin/bash