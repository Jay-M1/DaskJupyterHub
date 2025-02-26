FROM jupyterhub/jupyterhub:latest

RUN apt-get update && apt-get install -y sudo
RUN pip install jupyterhub jupyterlab dockerspawner jupyterhub-ldapauthenticator
RUN pip3 install dask[complete]

COPY jupyterhub_config.py /srv/jupyterhub/jupyterhub_config.py
COPY jupyter.token /srv/jupyterhub/jupyter.token