#!/bin/bash
# Execute the notebook using nbconvert.
echo "Running the notebook..."
jupyter nbconvert --to notebook --execute /home/jovyan/work/gateway.ipynb --output /home/jovyan/your_notebook_executed.ipynb

# Start the Jupyter Notebook server
echo "Starting the Jupyter Notebook server..."
exec start-notebook.sh
