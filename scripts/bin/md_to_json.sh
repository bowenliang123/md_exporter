#!/bin/bash

# 引入通用脚本
source "$(dirname "${BASH_SOURCE[0]}")/common.sh"

# 运行Python脚本
run_python_script "md_to_json.py" "$@"
