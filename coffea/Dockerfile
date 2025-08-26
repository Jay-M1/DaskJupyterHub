FROM coffeateam/coffea-base-almalinux9@sha256:0199f2f3014499fc6518e4dc1fd9da21d7ba0e544e8b8dc184a1afee056ab72b

RUN python3.10 -m venv /opt/python310-venv
RUN /opt/python310-venv/bin/pip install --upgrade pip && \
    /opt/python310-venv/bin/pip install \
    dask==2024.1.0 \
    distributed==2024.1.0 \
    dask-jobqueue==0.8.1 \
    dask-gateway==2024.1.0 \
    lz4 \
    msgpack \
    tornado
ENV PATH="/opt/python312-venv/bin:$PATH"
