#!/bin/bash

# Get the absolute path of the directory containing the script
function get_script_dir() {
    echo "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
}

# Get the project root directory
function get_project_root() {
    local script_dir="$(get_script_dir)"
    # When running from the scripts directory, go up one directory
    # When running from the test/bin directory, the run_python_script function will cd to the correct directory
    local project_root="$(dirname "$script_dir")"
    echo "$project_root"
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
    
    local original_dir="$(pwd)"
    local project_root="$(get_project_root)"
    local script_path="scripts/parser/$script_name"
    
    # Convert relative paths to absolute paths
    local abs_args=()
    local i=0
    while [[ $i -lt $# ]]; do
        local arg="${@:i+1:1}"
        if [[ "$arg" == --* ]] || [[ "$arg" == -* && ${#arg} -eq 2 ]]; then
            # This is an option (long or short), add it as-is
            abs_args+=("$arg")
            i=$((i+1))
            # Check if this option has a value
            if [[ $i -lt $# ]]; then
                local next_arg="${@:i+1:1}"
                if [[ "$next_arg" != --* ]] && [[ "$next_arg" != -* ]]; then
                    # This is the value for the option
                    if [[ "$next_arg" == /* ]]; then
                        # Already an absolute path
                        abs_args+=("$next_arg")
                    else
                        # Convert relative path to absolute path using original directory
                        abs_args+=("$original_dir/$next_arg")
                    fi
                    i=$((i+1))
                fi
            fi
        else
            # This is a non-option argument (file path)
            if [[ "$arg" == /* ]]; then
                # Already an absolute path
                abs_args+=("$arg")
            else
                # Convert relative path to absolute path using original directory
                abs_args+=("$original_dir/$arg")
            fi
            i=$((i+1))
        fi
    done
    
    # Check if uv is installed
    if command -v uv &> /dev/null; then
        echo "Using uv package manager..."
        cd "$project_root"
        # Set PYTHONPATH to include project root
        export PYTHONPATH="$project_root:$PYTHONPATH"
        # install Python dependencies with uv
        uv sync
        # run the script
        uv run python "$script_path" "${abs_args[@]}"
    else
        # Check Python version
        check_python_version

        echo "uv not found, using pip..."
        cd "$project_root"
        # Set PYTHONPATH to include project root
        export PYTHONPATH="$project_root:$PYTHONPATH"
        pip install -r requirements.txt
        python "$script_path" "${abs_args[@]}"
    fi
}