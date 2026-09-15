# Incident: Central-Manager-Umzug condorcentral → etprain

**Symptom:** `Spawn failed: ERROR: Can't find address of local schedd`.

**Root Cause:** Pool-Central-Manager umgezogen auf `etprain.etp.kit.edu`, aber die in die Images gebackenen Configs (`jupy/` und `rocky/configs/condor/config.d/0010.node_base.cfg`) zeigten noch auf `condorcentral.etp.kit.edu`. Ohne erreichbaren Collector kein Schedd-Ad → irreführender Schedd-Fehlertext (Schedd selbst lief gesund).

Diagnose: `docker exec jupyterhub-htcondor-jupyterhub-1 condor_status -schedd`.

**Fix:**
```diff
-CentralManager = condorcentral.etp.kit.edu
+CentralManager = etprain.etp.kit.edu
```
in beiden Dateien, dann `docker compose build jupyterhub htrocky && docker compose up -d --no-deps jupyterhub htrocky`.

**Bekannter Rest-Drift (bewusst nicht angefasst):** `0021.security.cfg` hat noch die alte Auth-Methoden-Reihenfolge (IDTOKENS muss vor PASSWORD stehen). Bisher unproblematisch, da FS-Auth an erster Stelle steht. Bei künftigem Auth-Fehler zuerst hier nachsehen.

**Nicht vergessen:** `/opt`-Checkout separat nachziehen (`admin-dokumentation-deploy-betrieb.md`).
