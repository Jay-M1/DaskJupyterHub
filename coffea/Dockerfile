FROM coffeateam/coffea-base-almalinux9@sha256:0199f2f3014499fc6518e4dc1fd9da21d7ba0e544e8b8dc184a1afee056ab72b

RUN mamba install --yes \
    -c conda-forge \
    conda-build=25.4.2 \
    dask=2025.4.1 \
    distributed=2025.4.1 \
    dask-jobqueue=0.9.0 \
    dask-gateway=2025.4.0 \
    && mamba clean --all --yes
