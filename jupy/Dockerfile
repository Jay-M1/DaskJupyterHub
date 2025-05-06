FROM jupyterhub/jupyterhub@sha256:b81d3265ace34fccba84dafa3dda3354bbcdb64a5bdca44b79849d10e29aa35b

RUN apt-get update && apt-get install -y sudo
RUN pip install jupyterhub jupyterlab dockerspawner jupyterhub-ldapauthenticator

COPY jupyterhub_config.py /srv/jupyterhub/jupyterhub_config.py
COPY jupyter.token /srv/jupyterhub/jupyter.token
