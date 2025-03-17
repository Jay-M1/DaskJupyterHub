FROM jupyter/base-notebook:latest

# Install any required libraries
RUN pip install dask-gateway

# Copy your local notebook into the container
COPY gateway.ipynb /home/jovyan/work

# Copy the startup script into the container
COPY run_notebook.sh /home/jovyan/work

# Ensure the startup script is executable
RUN chmod +x /home/jovyan/work/run_notebook.sh

# # Set the startup script as the default command
# CMD ["/home/jovyan/work/run_notebook.sh"]
