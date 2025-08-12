FROM rockylinux/rockylinux@sha256:767f30c94a9a43e46719408f877fb4eb91cea98401dd76a23abfc345ae5cb4ad

# Accept SHA1 signature keys for HTCondor Repo signing key
RUN update-crypto-policies --set DEFAULT:SHA1

RUN rpm --import http://research.cs.wisc.edu/htcondor/yum/RPM-GPG-KEY-HTCondor
RUN dnf install -y https://research.cs.wisc.edu/htcondor/repo/24.x/el9/x86_64/release/htcondor-release-24.x-1.el9.noarch.rpm

RUN dnf -y install epel-release authconfig nscd sssd git sudo procps && dnf clean all
RUN dnf config-manager --set-enabled crb
RUN dnf -y install condor && dnf clean all

# Enable LDAP auth
COPY --chmod=600 configs/sssd.conf /etc/sssd/sssd.conf
COPY --chmod=600 configs/nscd.conf /etc/nscd.conf
COPY configs/nsswitch.conf /etc/nsswitch.conf
RUN authconfig --enablesssd --update


RUN dnf -y install \
    gcc \
    make \
    wget \
    openssl-devel \
    bzip2-devel \
    libffi-devel \
    zlib-devel \
    sqlite-devel \
    xz-devel \
    ncurses-devel \
    readline-devel \
    tk-devel \
    gdbm-devel \
    libuuid-devel \
    libnsl2 \
    libtirpc-devel \
    && dnf clean all


# Install Python 3.12 from source
RUN wget https://www.python.org/ftp/python/3.12.4/Python-3.12.4.tgz \
    && tar xzf Python-3.12.4.tgz \
    && cd Python-3.12.4 \
    && ./configure --enable-optimizations \
    && make -j$(nproc) \
    && make altinstall \
    && cd .. \
    && rm -rf Python-3.12.4 Python-3.12.4.tgz

ENV PATH="/usr/local/bin:$PATH"

# Use pip for Python 3.12 to install Dask Gateway
RUN python3.12 -m ensurepip \
    && python3.12 -m pip install --upgrade pip --no-cache-dir \
    && python3.12 -m pip install --no-cache-dir \
    dask-gateway==2024.1.0 \
    dask==2024.1.0 \
    distributed==2024.1.0 \
    'dask-gateway-server' \
    async_timeout \
    'SQLAlchemy<2.0' \
    lz4 \
    msgpack \
    tornado
ARG GIT_REPO_VERSION=unknown
RUN python3.12 -m pip install --no-cache-dir git+https://github.com/Jay-M1/dask-gateway-htcondor.git

COPY configs/dask-gateway-server-config.py /srv/dask-gateway-server-config.py

# Configure HTCondor
COPY configs/condor/config.d /etc/condor/config.d
COPY configs/condor/tokens.d /etc/condor/tokens.d
RUN chmod 600 /etc/condor/tokens.d/*
RUN mkdir -m 1777 /var/lib/condor/fs_auth

COPY --chmod=777 test.sh /tmp/test.sh
COPY --chmod=666 job.jdl /tmp/job.jdl
RUN mkdir -m 1777 /tmp/logs

# Add Tini
ENV TINI_VERSION=v0.19.0
ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /tini
RUN chmod +rx /tini

COPY init.sh /srv/init.sh
RUN chmod +x /srv/init.sh

RUN useradd -m jovyan
RUN mkdir -p /tmp/.dask-gateway && chmod 777 /tmp/.dask-gateway

WORKDIR /srv
ENTRYPOINT ["/tini", "-s", "--", "/srv/init.sh"]
