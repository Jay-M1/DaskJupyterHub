FROM jupyter/base-notebook:latest

RUN pip install dask-gateway

WORKDIR /home/jovyan/work

COPY . .

CMD ["/home/jovyan/work/run_notebook.sh"]
