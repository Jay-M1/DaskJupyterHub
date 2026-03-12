# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Is

A self-hosted JupyterHub deployment for high-energy physics (HEP) analysis at KIT/ETP, integrated with HTCondor for distributed computing via Dask Gateway. The stack runs in Docker Swarm with overlay networking.

## Build and Deploy

**Full restart (destructive — stops all containers, clears networks/images, reinitializes swarm):**
```bash
bash restart.sh
```
This script handles: copying `requirements.txt` to subdirectories, copying the local `dask-gateway-htcondor` package into the build context, stopping all containers, leaving/re-initializing the Docker Swarm at `129.13.101.141`, rebuilding, and bringing services up.

**Rebuild htrocky after local backend changes (no full reset):**
```bash
cp -r /home/jmustafi/dask-gateway-htcondor/dask-gateway-htcondor/ rocky/dask-gateway-htcondor/
docker compose build htrocky && docker compose up -d --no-deps htrocky
```

**Rebuild a single service:**
```bash
docker compose build jupyterhub   # or: notebook, nginx, htrocky
docker compose up -d --no-deps jupyterhub
```

## Architecture

Four Docker services communicating over the `jupyternet` overlay network:

| Service | Image | Purpose |
|---|---|---|
| `jupyterhub` | `my_jupyterhub-jupyterhub` | JupyterHub hub server (port 8555) |
| `notebook` | `jnotebook_image` | Single-user notebook server spawned per user |
| `htrocky` | `my_rocky_image` | Dask Gateway server + HTCondor submit node (ports 8000, 9618) |
| `nginx` | `nginx_image` | TLS reverse proxy (port 443 → jupyterhub:8555, /clusters/ → htrocky:8000) |

**Key design decisions:**
- `htrocky` runs with `network_mode: host` so it can reach the HTCondor pool directly; all other services use the overlay network.
- JupyterHub uses `DockerSpawner` to launch `jnotebook_image` containers into the `my_jupyterhub_jupyternet` network. Home directories are bind-mounted: `/home/{username}` → `/home/{username}`.
- Auth is via LDAP (`ldap.etp.kit.edu`, port 636 TLS) against `dc=ekp,dc=physik,dc=uni-karlsruhe,dc=de`. UID/GID/username are pulled from LDAP auth state and injected as `NB_UID`/`NB_GID`/`NB_USER` env vars into spawned containers.
- Dask Gateway authenticates back to JupyterHub via `JUPYTERHUB_API_TOKEN` (shared through `.env`).
- Workers and schedulers run as HTCondor Docker universe jobs using `uhsur/coffea-base-almalinux9:latest`.
- Port 8000 on bms1 must be open in the firewall so execute nodes can reach the gateway API.

## Staging Directories

Two directories are used for per-cluster temporary files, both under `/home/jmustafi/dask-gateway-staging/` (temporary location until admin provides a shared path like `/var/lib/dask-gateway/`):

| Path | Purpose |
|---|---|
| `/home/jmustafi/dask-gateway-staging/{username}/` | TLS certs per cluster (gateway `staging_directory`) |
| `/home/jmustafi/dask-gateway-staging/{username}/htcondor/` | Job scripts and logs per cluster (`htcondor_staging_directory`) |

Both are created automatically per user when a cluster starts. A cron job cleans up subdirectories older than 1 day at 3am daily.

## Requirements Management

`requirements.txt` at the repo root is the single source of truth. `restart.sh` copies it to `rocky/` and `jupy/notebook/` before building. If you update dependencies, edit the root `requirements.txt` only — the copies in subdirectories are overwritten on each restart.

The `rocky` container uses Python 3.12 (built from source); the `notebook` container uses Python 3.10 (built from source) in `/opt/venv310`. Both install from the same `requirements.txt`, which includes coffea, dask-gateway, awkward, hist, fsspec-xrootd, and xrootd for HEP data analysis.

## Configuration Files

- `jupy/jupyterhub_config.py` — JupyterHub config (spawner, LDAP auth, Dask Gateway service registration). Mounted into the container at runtime, so edits take effect after `docker compose restart jupyterhub`.
- `rocky/configs/dask-gateway-server-config.py` — Dask Gateway config baked into the image. Points to HTCondor backend, sets worker resources (2G RAM, 1 core), and references `bms1.etp.kit.edu:8555` as the JupyterHub API URL.
- `nginx/nginx.conf` — Nginx TLS termination. Uses self-signed certs in `nginx/certs/`. Routes `/clusters/` to `host.docker.internal:8000` (the htrocky container via host networking).
- `rocky/configs/` — SSSD/NSCD/NSSwitch configs for LDAP user resolution inside the Rocky container.

## Environment

A `.env` file (not in git) must exist with at least `JUPYTERHUB_API_TOKEN`. This token is shared between `jupyterhub` and `htrocky` services.

## Testing the HTCondor Backend

Tests live in `rocky/dask-gateway-htcondor/tests/`. Run them inside the source tree:
```bash
cd rocky/dask-gateway-htcondor
pytest tests/
```
Uses `pytest-mock`; tests mock filesystem and uid operations so they run without a real HTCondor pool.

## Owned External Repositories

Two external resources used in this stack are owned by the repo author and can be modified:

- **`github.com/Jay-M1/dask-gateway-htcondor`** — The HTCondor backend for Dask Gateway. Installed in the `htrocky` image from the **local copy** at `rocky/dask-gateway-htcondor/` (copied from `/home/jmustafi/dask-gateway-htcondor/dask-gateway-htcondor/` by `restart.sh`). Edit locally and rebuild — no git push required for deployment.
- **`uhsur/coffea-base-almalinux9:latest`** (Docker Hub) — The worker/scheduler image used by HTCondor Docker universe jobs, configured in `rocky/configs/dask-gateway-server-config.py`. Changes to the Python environment, coffea version, or dependencies available on workers should be made in that image. To rebuild and push: build from `~/my_jupyterhub/coffea-backup/`, tag as `uhsur/coffea-base-almalinux9:latest`, and push to Docker Hub (see `upload_image.sh`).

## Systemd Service

`jupyterhub.service` in this repo should be installed to auto-start the stack on boot:
```bash
sudo cp jupyterhub.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable jupyterhub.service
```
On boot it runs `docker compose up -d` (not the destructive `restart.sh`). Run `restart.sh` manually only when a full rebuild is needed.

## HEP Analysis Notebooks

- `CoffeaDemoZPeak.ipynb` — Example Z→μμ analysis using coffea + Dask Gateway on HTCondor.
- `fileset.py` — XRootD file paths for CMS Run2018A DoubleMuon NANOAOD data (RWTH Aachen redirector).
- `Zmumu.root` — Local ROOT file for testing without XRootD.
