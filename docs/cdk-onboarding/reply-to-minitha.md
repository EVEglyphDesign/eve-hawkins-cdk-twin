# Reply to CDK — Data Your Way Extract prerequisites

**To:** Minitha Anand Kadimi, Implementation Support Rep, Professional Services, CDK Global
**From:** Dany Thériault, EVEglyphDesign — Hawkins Twin Platform
**Attachment to send:** [`evidence/2026-08-28-luke-sftp-probe-attempt-3-vpn-on-complete.txt`](evidence/2026-08-28-luke-sftp-probe-attempt-3-vpn-on-complete.txt) — canonical probe log (VPN engaged, all four commands captured end-to-end including the full `sftp` error).

**Kept in repo for our own record only:**
- [`evidence/2026-08-28-luke-sftp-probe-attempt-1-vpn-off.txt`](evidence/2026-08-28-luke-sftp-probe-attempt-1-vpn-off.txt) — first attempt, VPN off (identical result)
- [`evidence/2026-08-28-luke-sftp-probe-attempt-2-vpn-on.txt`](evidence/2026-08-28-luke-sftp-probe-attempt-2-vpn-on.txt) — second attempt, VPN on but terminal capture cut off mid-`sftp`

**Date drafted:** 2026-08-28
**Status:** three probe runs complete. All three terminate at the same CDK-upstream hop (`ae9.lr5-nyc6.ip4.gtt.net`, `89.149.142.105`) and produce `Connection timed out` on 22/tcp. Diagnosis is definitive: block sits at CDK's SFTP edge, not at Peterbilt's outbound firewall, and the VPN state does not change it. Send attempt 3 to Minitha. Awaiting Luke's phone and email to fill in the admin block.

---

## Reply text

> Hi Minitha,
>
> Attached is the probe log you requested, captured from Luke Weatherbie's CDK
> Drive workstation on the Peterbilt Atlantic network (`lweatherbie.PETERBILT`,
> Windows 10.0.26200.9106).
>
> **Result summary:**
>
> - `ping dataexportsftp.cdk.com` — 4/4 packets lost (100%)
> - `ping 192.224.101.40` — 4/4 packets lost (100%)
> - `tracert 192.224.101.40` — completes 9 hops through GTT's New York core
>   (`ae9.lr5-nyc6.ip4.gtt.net`, `89.149.142.105`), then every hop from 10
>   through 30 returns `Request timed out`
> - `sftp 192.224.101.40:22` — `ssh: connect to host 192.224.101.40 port 22:
>   Connection timed out` / `Connection closed`
>
> The trace shows our traffic reaches your upstream provider (GTT NY) cleanly;
> the block sits at your SFTP edge. **Please add Peterbilt Atlantic's public
> egress IP `143.105.101.188` to the Data Export SFTP allowlist so we can
> proceed.**
>
> On the other two items:
>
> - **Course 6432** — Luke is enrolling in *Data Your Way: Getting Started with
>   the Data Export Tool* on CDK Global University.
> - **Data Export Admin:**
>   - Name: Luke Weatherbie
>   - Role: Data Export Admin, Peterbilt Atlantic
>   - Phone: _[fill Luke's phone]_
>   - Email: _[fill Luke's email]_
>
> Thank you,
> Dany Thériault
> EVEglyphDesign — Hawkins Twin Platform

---

## Interpretation of the probe log (for our own record)

| Command | Result | Diagnostic |
|---|---|---|
| `ping dataexportsftp.cdk.com` → `192.224.101.40` | 4/4 lost | ICMP silently dropped at CDK edge (normal for enterprise SFTP) |
| `ping 192.224.101.40` | 4/4 lost | Same block confirmed at IP layer |
| `tracert 192.224.101.40` | 9 hops OK through GTT NY, then 21× `Request timed out` | Path is clean out of the dealership through GTT; block sits at hop 10+, which is CDK's edge or the last hop before it |
| `sftp 192.224.101.40:22` | `Connection timed out` | Load-bearing evidence — port 22 is not open to `143.105.101.188` |

**Peterbilt Atlantic public egress IP:** `143.105.101.188` (per Dany, 2026-08-28)
**Peterbilt Atlantic workstation user:** `lweatherbie.PETERBILT` (Windows 10.0.26200.9106)
**Peterbilt Atlantic local LAN gateway:** `192.168.1.1` → carrier CGNAT `100.64.0.1` → `206.224.75.x` → GTT

The screenshot proves the block is CDK-side. Nothing else moves — no course completion, no admin credentials, no Azure landing wiring — until CDK opens 22/tcp to `143.105.101.188`.
