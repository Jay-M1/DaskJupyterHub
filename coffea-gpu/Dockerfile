# GPU variant of the worker image: identical Python stack plus CuPy.
# The cupy-cuda12x wheel bundles its CUDA runtime; it only needs the
# host NVIDIA driver (libcuda) inside the container at run time.
#
# Baut auf dem versionierten CPU-Worker-Image (coffea-backup/Dockerfile)
# auf, nicht auf coffeateam/coffea-base-almalinux9 direkt, damit CPU- und
# GPU-Worker denselben dask/msgpack/tornado-Stand haben. Laeuft, anders
# als das CPU-Image, im HTCondor Container-Universe via Apptainer
# (container_image = docker://...-gpu), um auf die Apptainer-only
# NEMO/GridKa-GPU-Drones zu matchen (siehe nemo-gpu-worker.md).
FROM uhsur/coffea-base-almalinux9:2026-07-09
RUN /opt/python310-venv/bin/pip install --no-cache-dir cupy-cuda12x
