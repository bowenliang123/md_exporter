#!/bin/bash

# Import common script
source "$(dirname "${BASH_SOURCE[0]}")/script_runner.sh"

# Run Python script
run_python_script "md_to_docx.py" "$@"
