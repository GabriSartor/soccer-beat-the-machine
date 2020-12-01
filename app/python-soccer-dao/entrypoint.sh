#!/bin/bash
set -euo pipefail

if [ -v DEV_MODE ]; then
    python init.py
fi

exec tail -f /dev/null
