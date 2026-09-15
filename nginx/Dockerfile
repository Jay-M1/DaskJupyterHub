FROM nginx:alpine

# nginx.conf wird fest ins Image gebacken, nicht bind-gemountet (anders als
# jupyterhub_config.py beim jupyterhub-Service). Eine Aenderung an
# nginx/nginx.conf auf dem Host wirkt daher erst nach:
#   docker compose build nginx && docker compose up -d --no-deps nginx
# Ein reines `docker compose restart nginx` liefert weiter die alte Config.
COPY nginx.conf /etc/nginx/nginx.conf
