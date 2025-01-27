FROM jupyterhub/jupyterhub:latest

# Install JupyterHub, JupyterLab, DockerSpawner, and DummyAuthenticator
RUN apt-get update && apt-get install -y sudo
RUN pip install jupyterhub jupyterlab dockerspawner jupyterhub-dummyauthenticator jupyterhub-ldapauthenticator
#RUN pip install jupyterhub-ldapauthenticator

# Copy the JupyterHub configuration file
COPY jupyterhub_config.py /srv/jupyterhub/jupyterhub_config.py
COPY jupyter.token /srv/jupyterhub/jupyter.token

#CMD ["sudo", "jupyterhub"]