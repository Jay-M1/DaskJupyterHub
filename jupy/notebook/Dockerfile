# CLIENT - Python 3.10 only, no conda
FROM jupyterhub/singleuser@sha256:3e8ad15629fb14d20e7cad06f6e8e1c26908c28b208bc35af8976a7efa446491

USER root

# Remove conda completely to slim image and prevent PATH conflicts
RUN rm -rf /opt/conda

# Install Python 3.10 system packages
RUN apt-get update && apt-get install -y wget build-essential libssl-dev zlib1g-dev \
    libncurses5-dev libncursesw5-dev libreadline-dev libsqlite3-dev libgdbm-dev \
    libdb5.3-dev libbz2-dev libexpat1-dev liblzma-dev tk-dev libffi-dev uuid-dev && \
    wget https://www.python.org/ftp/python/3.10.17/Python-3.10.17.tgz && \
    tar xzf Python-3.10.17.tgz && \
    cd Python-3.10.17 && \
    ./configure --enable-optimizations --prefix=/usr/local && \
    make -j$(nproc) && make altinstall && \
    cd .. && rm -rf Python-3.10.17*

# Create Python 3.10 virtual environment
RUN python3.10 -m venv /opt/venv310

COPY requirements.txt .

# Upgrade pip and install all needed packages in venv
RUN /opt/venv310/bin/pip install --upgrade pip && \
    /opt/venv310/bin/pip install --no-cache-dir -r requirements.txt

# Register Python 3.10 kernel in Jupyter
RUN /opt/venv310/bin/python -m ipykernel install --name python310 --display-name "Python 3.10 (venv310)"

# Remove all notebook startup hooks (no conda activation, no PATH overrides)
RUN rm -rf /usr/local/bin/start-notebook.d/* && \
    rm -rf /usr/local/bin/before-notebook.d/*

# Ensure PATH points to venv and symlink important binaries
ENV PATH="/opt/venv310/bin:$PATH"
ENV PYTHONPATH="/opt/venv310/lib/python3.10/site-packages"
ENV JUPYTER_PREFER_ENV_PATH=1

RUN ln -sf /opt/venv310/bin/jupyterhub-singleuser /usr/local/bin/jupyterhub-singleuser && \
    ln -sf /opt/venv310/bin/jupyterhub /usr/local/bin/jupyterhub && \
    ln -sf /opt/venv310/bin/jupyter /usr/local/bin/jupyter

# Set permissions
RUN chmod -R 755 /opt/venv310

USER $NB_USER

HEALTHCHECK NONE
