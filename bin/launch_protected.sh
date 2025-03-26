#!/bin/bash

# =====================================================
# TGDK :: DominanceX Launcher
# AGENT: H6
# MODE: Desktop / Mobile Adaptive
# LICENSE: BFE-TGDK-022ST
# =====================================================

# Auto-detect mobile shell environment
if [[ "$OSTYPE" == "android"* || "$TERMUX_VERSION" != "" ]]; then
    export DOMINANCEX_MODE="MOBILE"
    export TGDK_HOME="$HOME/Makeshift"
    echo "[DominanceX] Mobile mode engaged via Termux or emulator"
else
    export DOMINANCEX_MODE="DESKTOP"
    export TGDK_HOME="$HOME/dominancex"
    echo "[DominanceX] Desktop mode active"
fi

# Log path prep
export TGDK_LOG="$TGDK_HOME/logs"
mkdir -p "$TGDK_LOG"

# Preload secure library if available
if [[ -f "$HOME/.dominancex/bin/libdominancex.so" ]]; then
    export LD_PRELOAD="$HOME/.dominancex/bin/libdominancex.so"
    echo "[DominanceX] LD_PRELOAD set to libdominancex.so" >> "$TGDK_LOG/launch.log"
fi

# Log execution mode
echo "[DominanceX] Launch Time: $(date)" >> "$TGDK_LOG/launch.log"
echo "[DominanceX] Execution Mode: $DOMINANCEX_MODE" >> "$TGDK_LOG/launch.log"

# Execute payload or passed arguments
if [[ -z "$1" ]]; then
    bash "$TGDK_HOME/src/.tails_ghost.sh"
else
    exec "$@"
fi