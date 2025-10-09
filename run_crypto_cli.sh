#!/bin/bash

# Wrapper script to run the crypto CLI with proper environment setup

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Set PYTHONPATH to include the project root
export PYTHONPATH="$SCRIPT_DIR:$PYTHONPATH"

# Run the crypto CLI with the venv python
"$SCRIPT_DIR/venv/bin/python" "$SCRIPT_DIR/cli/main_crypto.py" "$@"

