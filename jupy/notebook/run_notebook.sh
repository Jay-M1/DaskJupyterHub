#!/bin/bash
set -e

echo "Running the notebook..."
jupyter nbconvert --to notebook \
  --execute /home/jovyan/work/gateway.ipynb \
  --output /home/jovyan/work/your_notebook_executed.ipynb \
  --ExecutePreprocessor.allow_errors=False \
  --log-level=INFO

echo "Notebook execution complete."

echo "Starting the Jupyter Notebook server..."
exec start-notebook.sh
