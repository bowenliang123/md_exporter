#!/bin/bash

# 获取脚本所在目录的绝对路径
function get_script_dir() {
    echo "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
}

# 获取项目根目录
function get_project_root() {
    local script_dir="$(get_script_dir)"
    echo "$(dirname "$(dirname "$script_dir")")"
}

# 检查Python版本是否大于等于3.11
function check_python_version() {
    local python_version
    local major
    local minor
    
    # 获取Python版本并提取主版本号和次版本号
    python_version=$(python --version 2>&1)
    if [[ $python_version =~ Python[[:space:]]+([0-9]+)\.([0-9]+) ]]; then
        major=${BASH_REMATCH[1]}
        minor=${BASH_REMATCH[2]}
    else
        echo "Error: Could not determine Python version from: $python_version"
        exit 1
    fi
    
    # 比较版本号
    if (( major < 3 )) || (( major == 3 && minor < 11 )); then
        echo "Error: Python version 3.11 or higher is required. Current version: $major.$minor"
        exit 1
    fi
}

# 运行Python脚本，处理依赖管理
function run_python_script() {
    local script_name="$1"
    shift
    
    local project_root="$(get_project_root)"
    local script_path="scripts/$script_name"
    
    # 检查Python版本
    check_python_version
    
    # 检查uv是否安装
    if command -v uv &> /dev/null; then
        echo "Using uv package manager..."
        cd "$project_root"
        uv sync
        uv run python "$script_path" "$@"
    else
        echo "uv not found, using pip..."
        cd "$project_root"
        pip install -r requirements.txt
        python "$script_path" "$@"
    fi
}