FROM coffeateam/coffea-base-almalinux9:python3.12

RUN python3.12 -m venv /opt/python312-venv
RUN /opt/python312-venv/bin/pip install --upgrade pip && \
    /opt/python312-venv/bin/pip install \
    dask==2024.1.0 \
    distributed==2024.1.0 \
    dask-jobqueue==0.8.1 \
    dask-gateway==2024.1.0 \
    lz4 \
    msgpack \
    tornado
ENV PATH="/opt/python312-venv/bin:$PATH"
