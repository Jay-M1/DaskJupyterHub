FROM jupyterhub/singleuser@sha256:3e8ad15629fb14d20e7cad06f6e8e1c26908c28b208bc35af8976a7efa446491

USER root
RUN ln -s /opt/conda/bin/python3 /usr/bin/python3

USER $NB_USER

RUN pip install dask-gateway
