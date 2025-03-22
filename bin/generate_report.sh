#!/bin/bash
LOG="$HOME/.dominancex/logs/blocked.log"
OUT="$HOME/.dominancex/logs/dominancex_report.txt"
echo "DominanceX Threat Report - $(date)" > "$OUT"
grep -a "BLOCKED" "$LOG" | cut -c1-90 | sort | uniq -c | sort -nr >> "$OUT"
echo "[+] Report generated at $OUT"
