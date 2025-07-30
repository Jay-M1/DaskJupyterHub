#!/bin/bash

echo ">> Hostname: $(hostname)"
echo ">> Python bin: $(which python3)"
python3 --version
echo ""

# Wenn venv existiert:
if [ -f /opt/python312-venv/bin/activate ]; then
    echo "Activating Python 3.12 venv..."
    source /opt/python312-venv/bin/activate
fi

echo ">> Final Python version:"
python3 --version

# Starte Dask-Scheduler explizit mit Python 3.12
exec python3.12 -m distributed.cli.dask_scheduler
