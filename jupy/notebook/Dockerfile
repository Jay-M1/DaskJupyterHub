FROM jupyter/base-notebook:latest

# Install any required libraries
RUN pip install dask-gateway

# Copy your local notebook into the container
COPY gateway.ipynb /home/jovyan/work

# Copy the startup script into the container
COPY run_notebook.sh /home/jovyan/work

# # Set the startup script as the default commandasdf
CMD ["/home/jovyan/work/run_notebook.sh"]
