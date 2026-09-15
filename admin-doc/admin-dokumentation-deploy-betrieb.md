# Deploy, Restart, Betrieb

## Vor jedem Eingriff: Nutzeraktivität prüfen

```bash
docker exec jupyterhub-htcondor-jupyterhub-1 sh -c \
  "python3 -c \"import sqlite3; c=sqlite3.connect('/srv/jupyterhub/state/jupyterhub.sqlite'); \
  print([r for r in c.execute('select name,last_activity from users')])\""
condor_q -allusers
```

## Rebuild

Configs/`nginx.conf` sind per `COPY` gebacken — Änderung braucht immer `docker compose build <service>`, nicht nur `up -d`.

## `dangerous_restart.sh`

Stoppt/entfernt **alle** Docker-Container/-Images auf dem Host (nicht nur diesen Stack!), re-initialisiert den Swarm. Nur für kaputten Compose/Swarm-Zustand, nie für normale Restarts.
