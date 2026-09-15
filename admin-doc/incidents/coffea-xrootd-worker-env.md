# Incident: coffea "Empty list provided to reduction"

**Symptom:** coffea-Preprocess über Dask-Gateway auf Remote-XRootD-Dateien bricht ab (mit `skipbadfiles=True`: alle Dateien scheitern beim Öffnen → leere Liste).

**Root Cause:** `client.run(set_env)` setzt das X509-Proxy-Env nur auf den zum Aufrufzeitpunkt bereits verbundenen Workern. Nach `cluster.scale(n)` später gestartete Worker bekommen es nie.

**Fix:** `WorkerPlugin`, dessen `setup()` das Env setzt (deckt aktuelle + künftige Worker ab):

```python
class GridEnvPlugin(WorkerPlugin):
    def setup(self, worker):
        import os
        os.environ["X509_USER_PROXY"] = "/home/<user>/.globus/x509up"
        os.environ["X509_CERT_DIR"] = "/cvmfs/grid.cern.ch/etc/grid-security/certificates"
        os.environ["X509_VOMS_DIR"] = "/cvmfs/grid.cern.ch/etc/grid-security/vomsdir"
client.register_plugin(GridEnvPlugin())
```

**Wichtig:** Env muss **vor** der ersten XRootD-Nutzung im Prozess gesetzt sein (Setup läuft bei Worker-Start) — nachträgliches Setzen auf einem bereits genutzten Worker hilft nicht mehr (`No protocols left to try`). Im Zweifel frischen Cluster nutzen.

Verwandt: abgelaufener Proxy erzeugt denselben Fehler trotz korrektem Env → `voms-proxy-info -timeleft` prüfen (`grid-cert-renewal.md`).
