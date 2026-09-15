# Incident: Abgelaufenes TLS-Zertifikat

**Symptom:** `NET::ERR_CERT_DATE_INVALID`. Prüfen: `echo | openssl s_client -connect bms1.etp.kit.edu:443 2>/dev/null | openssl x509 -noout -dates`.

**Root Cause:** `authenticator = standalone` brauchte Port 80 für die Challenge, aber nur 443 war published → Renewal scheiterte monatelang unbemerkt. Zusätzlich fehlte ein Deploy-Hook (nginx bindet `/etc/letsencrypt` read-only, hätte ein erfolgreiches Renewal nicht automatisch übernommen).

**Fix:**
- `nginx.conf`: Port-80-Block für `/.well-known/acme-challenge/` (Webroot), Rest → 301 https. `docker-compose.yml`: `"80:80"` + Webroot-Mount. (Nach Config-Änderung: `docker compose build nginx`, nicht nur `up -d`.)
- Certbot auf `webroot`-Authenticator umgestellt, Deploy-Hook (`docker compose restart nginx`) angelegt.
- `certbot renew --dry-run` verifiziert die komplette Kette.

Läuft seitdem automatisch (`certbot-renew.timer`, alle 12h).
