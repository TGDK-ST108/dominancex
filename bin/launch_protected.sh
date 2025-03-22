#!/bin/bash
export LD_PRELOAD=$HOME/.dominancex/bin/libdominancex.so
exec "$@"
