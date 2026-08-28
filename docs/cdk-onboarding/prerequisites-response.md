# CDK Data Your Way Extract — Prerequisites Response

**Correspondence:** Minitha Anand Kadimi, Implementation Support Rep, Professional Services, CDK Global
**Received:** August 2026, WarrantyGENE / Peterbilt Atlantic lane
**Owner:** Luke Weatherbie (Data Export Admin, designated)
**Status:** probes complete 2026-08-28 — CDK-side firewall block confirmed; awaiting CDK allowlist of `143.105.101.188`. Reply drafted at [`reply-to-minitha.md`](reply-to-minitha.md).

**Peterbilt Atlantic public egress IP:** `143.105.101.188`
**Evidence:** [`evidence/2026-08-28-luke-sftp-probe.txt`](evidence/2026-08-28-luke-sftp-probe.txt) — probe run from `lweatherbie.PETERBILT` at 2026-08-28. `sftp 192.224.101.40:22` returned `Connection timed out`; tracert path clean through GTT NY to hop 9, blocked hop 10+.

---

## The three prerequisites CDK asked for

### 1. Network probes from the accessing host

CDK requires a screenshot of the following four commands executed **from the machine that will connect to the SFTP server** — not a laptop, not this scratch environment, but the host that will hold the SFTP client long-term.

For Peterbilt Atlantic, that host is a VM inside the `dany-sandbox` resource group in the `atopos.io` Azure directory. The probe script that runs the four commands and captures the log is committed at [`extract/bin/01_cdk_sftp_probe.sh`](../../extract/bin/01_cdk_sftp_probe.sh) — one invocation, one log file, screenshot the terminal.

The four commands (as CDK specified them):

```
ping dataexportsftp.cdk.com
ping 192.224.101.40
tracert 192.224.101.40
sftp 192.224.101.40:22
```

**Owner action:** Luke runs `01_cdk_sftp_probe.sh` on the Azure puller host once it is stood up, captures the terminal screenshot, and sends it to CDK.

### 2. CDK Global University course 6432

CDK Customer Care will not assist with the Data Export Tool until course 6432 —
*"Data Your Way: Getting Started with the Data Export Tool"* — has been completed by the operator.

- **Course:** 6432 — Data Your Way: Getting Started with the Data Export Tool
- **Portal:** [CDK Global University](https://cdkglobaluniversity.com/) (login required; self-registration path is documented in CDK's onboarding email)
- **Assigned learner:** Luke Weatherbie

**Owner action:** Luke self-registers if he does not already have a CDK Global University login, enrolls in course 6432, and completes it. Completion certificate becomes the evidence for CDK.

### 3. Data Export Admin — designated contact

CDK requires the name, phone, and email of the person who will hold the Data Export tool
and be the point of contact for CDK Customer Care.

| Field | Value |
|---|---|
| Name | Luke Weatherbie |
| Role | Data Export Admin, Peterbilt Atlantic / Extreme Torque Motorsports |
| Phone | `PENDING` — to be filled from Luke before reply is sent |
| Email | `PENDING` — to be filled from Luke before reply is sent |
| Public egress IP (for CDK allowlist) | `143.105.101.188` |

**Owner action:** Populate phone and email in this file, then send the reply.

---

## Landing-zone context (for CDK's benefit, not part of the reply)

Once CDK provisions the SFTP account, the pull flows into the pre-existing Azure sandbox:

- **Directory:** `atopos.io`
- **Resource group:** `dany-sandbox`
- **Landing DB:** `dany-sandbox-db.postgres.database.azure.com`, database `sandbox`, PostgreSQL 18 with `pgvector` and `pg_stat_statements` enabled
- **User:** `pgadmin` (password held out-of-band; sourced via `PGPASSWORD` env var, never in files)
- **SSL:** `verify-full` required
- **Network posture:** IP-allowlist per client; no broad "allow all Azure services" rule
- **PGP key custody:** Hawkins generates and retains the private key; only the public key ever goes to CDK (per the CDK-export custody canon in [`projects/peterbilt-atlantic-digital-twin`](https://raw.githubusercontent.com/EVEglyphDesign/hawkins-twin-platform/main/knowledge/projects/peterbilt-atlantic-digital-twin.md))

The Postgres targets are recorded in [`extract/config/targets.yaml`](../../extract/config/targets.yaml) under the `landing_zone` block. The ingest step consuming CDK's decrypted extracts is [`extract/bin/40_ingest_exports.py`](../../extract/bin/40_ingest_exports.py).

---

## Reply draft to Minitha (fill phone/email, then send)

> Hi Minitha,
>
> Thank you for the onboarding note. Three responses, one per item:
>
> 1. **Network probes.** The screenshot of the four commands
>    (`ping dataexportsftp.cdk.com`, `ping 192.224.101.40`, `tracert 192.224.101.40`,
>    `sftp 192.224.101.40:22`) will be sent from the host that will access the
>    SFTP server, once that host is provisioned in our Azure landing zone.
>    Expected within the week.
>
> 2. **Course 6432.** Luke Weatherbie is enrolling in *Data Your Way: Getting Started with
>    the Data Export Tool* and will complete it before requesting Customer Care support.
>
> 3. **Data Export Admin.** Our designated contact is:
>
>    - **Name:** Luke Weatherbie
>    - **Role:** Data Export Admin, Peterbilt Atlantic / Extreme Torque Motorsports
>    - **Phone:** _[insert Luke's phone]_
>    - **Email:** _[insert Luke's email]_
>
> Please route Data Export Tool provisioning and any subsequent CDK Customer Care
> correspondence to Luke.
>
> Thank you,
> Dany Thériault
> EVEglyphDesign — Hawkins Twin Platform lane
