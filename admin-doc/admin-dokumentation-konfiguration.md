# Konfigurationsdateien

## `jupy/jupyterhub_config.py`

- Hub-State (`db_url`, `cookie_secret_file`, `auth_state.key`) → `/srv/jupyterhub/state` (Volume `hub-state`).
- `LDAPAuthenticator`, `allow_all = True`.
- `c.Spawner.ip = "0.0.0.0"` (Default `127.0.0.1` wäre auf Execute-Node unerreichbar).
- `HTCondorNotebookSpawner(CondorSpawner)`:
  - `exec_prefix = "sudo -n -u {username} -H"` — **nicht** `os.seteuid()` (ändert nur effektive, nicht reale UID; Condors FS-Auth braucht real).
  - `batch_script`: vanilla-Universe + `+WantContainer`/`+ContainerImage` (Docker-Universe verbietet root, bricht `gosu`).
  - `initialdir` (nicht `remote_initialdir`), `docker_network_type = host`, `environment = {environment}` (ohne äußere Quotes, sonst bricht es bei Werten mit `"`).
  - `get_env()` überschreibt nur `JUPYTERHUB_API_URL`/`_ACTIVITY_URL` (Port 8081 ist cross-node nicht erreichbar) — **nicht** global `hub_connect_url` setzen (bricht die Proxy-Route zum Hub).

## `docker-compose.yml`

- `jupyterhub`/`htrocky`: `network_mode: host`, Condor-Auth-Mounts vom Host.
- `htrocky`: Build-Arg `GIT_REPO_VERSION` pinnt den Backend-Commit.
- Compose-Projektname fest `jupyterhub-htcondor` (stabil über beide Checkouts hinweg).
- Volume `hub-state`.

## `rocky/dask-gateway-server-config.py`

- `backend_class` aus separatem Git-Repo (`pip install git+...@${GIT_REPO_VERSION}`), nicht lokal.
- `HTCondorClusterConfig.docker_image` wirkt für Scheduler **und** Worker. `scheduler_docker_image` ist **tot**, wird ignoriert.

## `rocky/dask-gateway-htcondor/.../htcondor.py` (separates Repo)

Baut Scheduler-/Worker-JDL, `docker_network_type = host`. Worker verbinden direkt zu `cluster.scheduler_address`, nicht über den Gateway-Proxy (im ETP-Subnetz unkritisch).

Ändern: lokalen Klon editieren → committen/pushen ins Backend-Repo → `GIT_REPO_VERSION` bumpen → `htrocky` neu bauen.

## `nginx/nginx.conf`

- `proxy_pass` **statisch**, keine Variable (`resolver 127.0.0.11` kennt `host.docker.internal` nicht).
- Port-80-Block für ACME-Challenge, Rest → 301 auf https.

## Image-Tags

Nie `:latest` als einzige Referenz — Execute-Nodes cachen Tags und ziehen nie neu.
