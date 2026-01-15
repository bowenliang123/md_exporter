#!/bin/bash

# Get the absolute path of the directory containing the script
function get_script_dir() {
    echo "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
}

# Get the project root directory
function get_project_root() {
    local script_dir="$(get_script_dir)"
    echo "$(dirname "$(dirname "$script_dir")")"
}

# Check if Python version is >= 3.11
function check_python_version() {
    local python_version
    local major
    local minor
    
    # Get Python version and extract major and minor version numbers
    python_version=$(python --version 2>&1)
    if [[ $python_version =~ Python[[:space:]]+([0-9]+)\.([0-9]+) ]]; then
        major=${BASH_REMATCH[1]}
        minor=${BASH_REMATCH[2]}
    else
        echo "Error: Could not determine Python version from: $python_version"
        exit 1
    fi
    
    # Compare version numbers
    if (( major < 3 )) || (( major == 3 && minor < 11 )); then
        echo "Error: Python version 3.11 or higher is required. Current version: $major.$minor"
        exit 1
    fi
}

# Run Python script with dependency management
function run_python_script() {
    local script_name="$1"
    shift
    
    local project_root="$(get_project_root)"
    local script_path="scripts/$script_name"
    
    # Check if uv is installed
    if command -v uv &> /dev/null; then
        echo "Using uv package manager..."
        cd "$project_root"
        # uv run automatically handles dependencies
        uv run python "$script_path" "$@"
    else
        # Check Python version
        check_python_version

        echo "uv not found, using pip..."
        cd "$project_root"
        pip install -r requirements.txt
        python "$script_path" "$@"
    fi
}