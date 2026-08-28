#!/usr/bin/env bash
# extract/bin/01_cdk_sftp_probe.sh
#
# Runs the four network commands CDK requires as evidence in the Data Your Way
# Extract onboarding (see docs/cdk-onboarding/prerequisites-response.md, item 1).
#
# Must be executed from the host that will hold the SFTP client long-term ---
# for Peterbilt Atlantic, that is the VM inside the `dany-sandbox` resource
# group in the `atopos.io` Azure directory --- so CDK sees the same egress path
# they will later allowlist.
#
# Produces one timestamped log the operator screenshots for CDK.
#
# Usage:
#     bash extract/bin/01_cdk_sftp_probe.sh
#
# On Linux hosts `tracert` is aliased to `traceroute`; on Windows use
# `wsl bash extract/bin/01_cdk_sftp_probe.sh` or run the four commands directly
# in `cmd.exe` / PowerShell --- CDK asked for `tracert` output specifically.

set -u  # unset variables are errors; do NOT set -e --- we want partial output
        # even when one probe fails, because that IS the diagnostic CDK asked for.

HOSTNAME_LC=$(hostname 2>/dev/null || echo unknown-host)
STAMP=$(date -u +%Y%m%d-%H%M%SZ)
LOG_DIR="$(cd "$(dirname "$0")/../out" && pwd)/probes"
LOG_FILE="${LOG_DIR}/cdk-sftp-probe-${HOSTNAME_LC}-${STAMP}.log"
mkdir -p "${LOG_DIR}"

# Portable tracert-equivalent picker.
TRACEROUTE_CMD=""
if command -v tracert >/dev/null 2>&1; then
  TRACEROUTE_CMD="tracert"
elif command -v traceroute >/dev/null 2>&1; then
  TRACEROUTE_CMD="traceroute"
else
  TRACEROUTE_CMD=""
fi

# Also try tcping / nc for the SFTP TCP-port check, because non-interactive sftp
# hangs at the password prompt --- we want the connect-vs-refuse signal, not
# a login. If neither is present, fall back to `sftp -o BatchMode=yes`.
TCP_CHECK_CMD=""
if command -v nc >/dev/null 2>&1; then
  TCP_CHECK_CMD="nc -z -w 5 -v"
elif command -v tcping >/dev/null 2>&1; then
  TCP_CHECK_CMD="tcping"
fi

banner () {
  echo ""
  echo "==================================================================="
  echo "$1"
  echo "==================================================================="
}

{
  echo "CDK Data Your Way Extract --- network prerequisites probe"
  echo "Host      : ${HOSTNAME_LC}"
  echo "Timestamp : ${STAMP} (UTC)"
  echo "Operator  : ${USER:-unknown}"
  echo "Purpose   : Evidence for CDK Global (Minitha Anand Kadimi)"
  echo ""

  banner "1. ping dataexportsftp.cdk.com"
  ping -c 4 dataexportsftp.cdk.com 2>&1 || true

  banner "2. ping 192.224.101.40"
  ping -c 4 192.224.101.40 2>&1 || true

  banner "3. tracert 192.224.101.40   (${TRACEROUTE_CMD:-not available on PATH})"
  if [ -n "${TRACEROUTE_CMD}" ]; then
    ${TRACEROUTE_CMD} 192.224.101.40 2>&1 || true
  else
    echo "SKIPPED --- neither 'tracert' nor 'traceroute' is on PATH."
    echo "Install traceroute (Linux: sudo apt install traceroute) or run"
    echo "'tracert 192.224.101.40' directly in Windows cmd.exe / PowerShell."
  fi

  banner "4. sftp 192.224.101.40:22   (TCP reachability probe, non-interactive)"
  if [ -n "${TCP_CHECK_CMD}" ]; then
    ${TCP_CHECK_CMD} 192.224.101.40 22 2>&1 || true
  else
    # BatchMode prevents the password prompt from hanging the log.
    sftp -o BatchMode=yes -o ConnectTimeout=10 -o StrictHostKeyChecking=accept-new \
         -P 22 anonymous@192.224.101.40 2>&1 </dev/null || true
  fi

  echo ""
  echo "==================================================================="
  echo "END OF PROBE --- screenshot this log for CDK."
  echo "Log written to: ${LOG_FILE}"
  echo "==================================================================="
} | tee "${LOG_FILE}"
