FROM jupyterhub/singleuser@sha256:3e8ad15629fb14d20e7cad06f6e8e1c26908c28b208bc35af8976a7efa446491

USER root
RUN ln -s /opt/conda/bin/python3 /usr/bin/python3

RUN python3.12 -m venv /opt/venv312
RUN /opt/venv312/bin/pip install --upgrade pip && \
    /opt/venv312/bin/pip install \
    dask==2025.4.1 \
    distributed==2025.4.1 \
    dask-jobqueue==0.9.0 \
    dask-gateway==2025.4.0

RUN chmod -R 755 /opt/venv312

USER $NB_USER

ENV PATH="/opt/venv312/bin:$PATH"
ENV PYTHONPATH="/opt/venv312/lib/python3.12/site-packages"

HEALTHCHECK NONE
