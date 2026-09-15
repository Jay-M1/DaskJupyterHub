# Troubleshooting

## Vorgehen

1. Betroffenheit klären (ein User? ganzer Stack?), Ebene identifizieren (Hub-Login → Spawn → Dask-Cluster → Job).
2. Logs lesen (siehe `admin-dokumentation.md`), dann Condor-Status prüfen.
3. Vor jedem Eingriff: Nutzeraktivität prüfen (`admin-dokumentation-deploy-betrieb.md`).

## HTCondor-Befehle

| Befehl | Zweck |
|---|---|
| `condor_q -submitter <user>` | eigene/fremde Jobs |
| `condor_q -better-analyze <id>` | warum idle |
| `condor_q -held -af HoldReason` | Hold-Grund |
| `condor_status` | Pool-Übersicht |
| `condor_history <id>` | abgeschlossene Jobs |
| `condor_ssh_to_job <id>` | Execute-Host, Container-FS via `/proc/<pid>/root` |

## Fehlerbilder

**Spawn failed, `Can't find address of local schedd`** — Collector unerreichbar (falscher Central Manager), nicht der Schedd selbst. Prüfen: `docker exec jupyterhub-htcondor-jupyterhub-1 condor_status -schedd`. → `incidents/central-manager-migration.md`.

**`Cannot access initial working directory`** — JDL nutzt `remote_initialdir` statt `initialdir` (vanilla-Universe).

**`GatewayClusterError` / `Permission denied: /var/lib/dask-gateway`** — `chmod 1777 /var/lib/dask-gateway`.

**Dask-Gateway `401 Unauthorized`** — Hub-DB nicht persistiert (verwaister Token). → `incidents/dask-gateway-401-hub-persistence.md`.

**Worker-Churn / sterben nach Cluster-Start** — Versionsdrift durch gecachte `:latest`-Tags. Fix: versionierte Tags, Kernpakete (msgpack/tornado/dask/distributed) gleich pinnen.

**coffea `Empty list provided to reduction`** — X509-Env fehlt auf (später gestarteten) Workern. Fix: `WorkerPlugin` statt `client.run()`. → `incidents/coffea-xrootd-worker-env.md`.

**TLS-Zertifikat abgelaufen** — prüfen: `echo | openssl s_client -connect bms1.etp.kit.edu:443 2>/dev/null | openssl x509 -noout -dates`. → `incidents/tls-zertifikat-erneuerung.md`.

## Diagnose-Cheatsheet

- `condor_ssh_to_job` landet auf dem **Host**, nicht im Container. Container-FS: `/proc/<pid>/root`, Env: `/proc/<pid>/environ`.
- Komplexe Kommandos zerbrechen an `condor_ssh_to_job`s `eval` → Skript-Datei ins NFS-Home legen, per Pfad aufrufen.
- `condor_config_val -name <node> -startd <KNOB>` liest Remote-Config ohne Login.
- Image-Tags werden nie neu gezogen — immer neuer Tag bei Updates.
- Für headless Tests: Wegwerf-venv (`uv`) mit exakt den Worker-Image-Versionen.

## Staging-Cleanup

`cleanup-dask-gateway-staging.sh` (Cronjob, täglich 3 Uhr) löscht verwaiste `/var/lib/dask-gateway/$USER/`-Unterordner. Aktiv = Verzeichnis ist `Iwd` eines laufenden Jobs (`condor_q -allusers -af Iwd`), nicht Zeitstempel (Job-Logs werden erst bei `ON_EXIT` geschrieben). `DRY_RUN=1` zum Testen. Räumt nur das eigene Verzeichnis des Cron-Users (Sticky-Bit 1777) — für alle User bräuchte es root-Cron.
