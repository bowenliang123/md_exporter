#!/bin/bash

# Import common script
source "$(dirname "${BASH_SOURCE[0]}")/script_runner.sh"

# Run Python script
run_python_script "cli_md_to_png.py" "$@"
