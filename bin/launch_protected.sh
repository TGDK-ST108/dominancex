#!/bin/bash

if [[ "$OSTYPE" == "android"* || "$TERMUX_VERSION" != "" ]]; then
    export DOMINANCEX_MODE="MOBILE"
    export TGDK_HOME="$HOME/Makeshift"
    echo "[DominanceX] Mobile mode engaged via Termux or shell emulator"
fi

export LD_PRELOAD=$HOME/.dominancex/bin/libdominancex.so
exec "$@"
