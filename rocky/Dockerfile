FROM rockylinux/rockylinux@sha256:767f30c94a9a43e46719408f877fb4eb91cea98401dd76a23abfc345ae5cb4ad

# Install base dependencies and create user
RUN dnf install -y sudo \
 && dnf update -y \
 && dnf -y swap curl-minimal curl \
 && dnf install -y vim python3 git \
 && dnf -y install dnf-plugins-core \
 && dnf -y config-manager --add-repo https://download.docker.com/linux/rhel/docker-ce.repo \
 && dnf -y install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin \
 && dnf clean all \
 && useradd -m -u 1000 jovyan

# Install HTCondor
RUN curl -fsSL https://get.htcondor.org | /bin/bash -s -- --no-dry-run

# Python setup and packages
ARG GIT_REPO_VERSION=unknown
RUN python3 -m ensurepip --default-pip \
 && python3 -m pip install --upgrade pip \
 && pip install --no-cache-dir \
    dask-gateway \
    'dask-gateway-server[local]' \
    'SQLAlchemy<2.0' \
    git+https://github.com/Jay-M1/dask-gateway-htcondor.git --no-cache-dir 

# Set up working directory and copy files
WORKDIR /work
COPY . .

# Set permissions
RUN chmod +x start.sh

# Expose required port and set default command
EXPOSE 9618
CMD ["./start.sh"]
