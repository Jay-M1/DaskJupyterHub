FROM jupyterhub/jupyterhub@sha256:b81d3265ace34fccba84dafa3dda3354bbcdb64a5bdca44b79849d10e29aa35b

RUN apt-get update && \
    apt-get install -y software-properties-common && \
    add-apt-repository ppa:deadsnakes/ppa && \
    apt-get update && \
    apt-get install -y python3.10 python3.10-venv python3.10-dev python3-pip && \
    rm -rf /var/lib/apt/lists/*

RUN python3.10 -m venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH"

RUN pip install --no-cache-dir jupyterhub jupyterlab dockerspawner jupyterhub-ldapauthenticator

WORKDIR /srv/jupyterhub

COPY jupyterhub_config.py jupyterhub_config.py
COPY jupyter.token jupyter.token
