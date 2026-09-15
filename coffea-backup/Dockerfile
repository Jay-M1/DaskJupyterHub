# Kein eigener Compose-Service: dieses Image wird gebaut und als
# uhsur/coffea-base-almalinux9:<tag> auf Docker Hub gepusht (siehe
# upload_image.sh), dann von HTCondor-Docker-Universe-Jobs referenziert
# (rocky/configs/dask-gateway-server-config.py) und matched nur auf die
# ETP-Docker-Execute-Nodes (keine GPUs dort). IMMER einen versionierten
# Tag verwenden, nie :latest: unterschiedlich gecachte :latest-Staende auf
# den Nodes fuehrten zuvor zu einem msgpack/tornado/dask-Versionsdrift und
# staendigem Worker-Churn.
FROM coffeateam/coffea-base-almalinux9@sha256:0199f2f3014499fc6518e4dc1fd9da21d7ba0e544e8b8dc184a1afee056ab72b

# Install development libraries needed for xrootd build
RUN dnf install -y \
    cmake \
    gcc \
    gcc-c++ \
    openssl-devel \
    zlib-devel \
    libuuid-devel \
    libxml2-devel \
    && dnf clean all

# Coffea-Base-Image bringt einen eigenen (aelteren) Conda-Compiler mit, der
# beim Bau der XRootD-Bindings im venv fehlschlaegt; erzwingt stattdessen
# den System-gcc.
ENV CC=/usr/bin/gcc
ENV CXX=/usr/bin/g++

# Remove conda compiler symlinks that interfere
RUN rm -f /usr/local/bin/cc /usr/local/bin/c++ 2>/dev/null || true

RUN python3.10 -m venv /opt/python310-venv

COPY requirements.txt .

RUN /opt/python310-venv/bin/pip install --upgrade pip && \
    /opt/python310-venv/bin/pip install --no-cache-dir -r requirements.txt

ENV PATH="/opt/python310-venv/bin:$PATH"
