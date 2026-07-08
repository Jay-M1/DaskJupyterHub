FROM jupyterhub/jupyterhub@sha256:b81d3265ace34fccba84dafa3dda3354bbcdb64a5bdca44b79849d10e29aa35b

RUN apt-get update && \
    apt-get install -y software-properties-common cmake gnupg wget && \
    add-apt-repository ppa:deadsnakes/ppa && \
    apt-get update && \
    apt-get install -y python3.10 python3.10-venv python3.10-dev python3-pip && \
    rm -rf /var/lib/apt/lists/*

RUN python3.10 -m venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH"

RUN pip install --no-cache-dir jupyterhub jupyterlab batchspawner jupyterhub-ldapauthenticator

# HTCondor client (condor_submit/condor_q/condor_rm) so the Hub can submit
# notebook servers as batch jobs into the same ETP pool htrocky already uses.
RUN wget -qO- https://htcss-downloads.chtc.wisc.edu/repo/keys/HTCondor-24.0-Key | gpg --dearmor -o /usr/share/keyrings/htcondor.gpg && \
    echo "deb [signed-by=/usr/share/keyrings/htcondor.gpg] https://htcss-downloads.chtc.wisc.edu/repo/ubuntu/24.0 jammy main" > /etc/apt/sources.list.d/htcondor.list && \
    apt-get update && \
    apt-get install -y htcondor && \
    rm -rf /var/lib/apt/lists/*

# Same pool config/tokens as htrocky (rocky/configs/condor), so condor_submit
# from inside this container reaches the same schedd/pool.
COPY configs/condor/config.d /etc/condor/config.d
COPY configs/condor/tokens.d /etc/condor/tokens.d

# LDAP/NSS bind (sssd), same purpose as htrocky's sssd (rocky/configs/sssd.conf):
# condor_submit runs here via `sudo -n -u <username>` (see jupyterhub_config.py,
# matching dask-gateway-server's own do_as_user() in
# dask_gateway_server/backends/jobqueue/base.py), and both sudo (to resolve
# the target user) and HTCondor's FS pool auth (to map the real uid the
# resulting process runs as back to a name) need NSS to see LDAP users.
RUN apt-get update && \
    apt-get install -y sssd sssd-ldap libnss-sss libpam-sss sudo && \
    rm -rf /var/lib/apt/lists/*
COPY --chmod=600 configs/sssd.conf /etc/sssd/sssd.conf
COPY configs/nsswitch.conf /etc/nsswitch.conf

COPY docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh
RUN chmod +x /usr/local/bin/docker-entrypoint.sh
ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]

WORKDIR /srv/jupyterhub

COPY jupyterhub_config.py jupyterhub_config.py
COPY jupyter.token jupyter.token

CMD ["jupyterhub"]
