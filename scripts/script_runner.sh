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

# Sanitize and validate input arguments to prevent shell injection
function sanitize_arg() {
    local arg="$1"
    # Reject arguments that contain shell metacharacters that could be dangerous
    if [[ "$arg" == *';'* ]] || [[ "$arg" == *'|'* ]] || [[ "$arg" == *'&'* ]] || \
       [[ "$arg" == *'<'* ]] || [[ "$arg" == *'>'* ]] || [[ "$arg" == *'('* ]] || \
       [[ "$arg" == *')'* ]] || [[ "$arg" == *'$'* ]] || [[ "$arg" == *'`'* ]] || \
       [[ "$arg" == *'"'* ]] || [[ "$arg" == *"'"* ]] || [[ "$arg" == *'*'* ]] || \
       [[ "$arg" == *'?'* ]] || [[ "$arg" == *'['* ]] || [[ "$arg" == *']'* ]] || \
       [[ "$arg" == *'{'* ]] || [[ "$arg" == *'}'* ]] || [[ "$arg" == *'~'* ]]; then
        echo "Error: Invalid argument containing potentially dangerous characters" >&2
        exit 1
    fi
    echo "$arg"
}

# Validate script name to ensure it only contains valid characters
function validate_script_name() {
    local script_name="$1"
    if [[ ! "$script_name" =~ ^[a-zA-Z0-9_]+\.py$ ]]; then
        echo "Error: Invalid script name" >&2
        exit 1
    fi
    # Ensure the script exists in the expected directory
    local script_path="scripts/parser/$script_name"
    local project_root="$(get_project_root)"
    if [[ ! -f "$project_root/$script_path" ]]; then
        echo "Error: Script not found: $script_name" >&2
        exit 1
    fi
    echo "$script_name"
}

# Run Python script with dependency management
function run_python_script() {
    local raw_script_name="$1"
    shift
    
    # Validate and sanitize script name
    local script_name="$(validate_script_name "$raw_script_name")"
    
    local original_dir="$(pwd)"
    local project_root="$(get_project_root)"
    local script_path="scripts/parser/$script_name"
    
    # Convert relative paths to absolute paths and sanitize all arguments
    local abs_args=()
    local i=0
    while [[ $i -lt $# ]]; do
        local raw_arg="${@:i+1:1}"
        local arg="$(sanitize_arg "$raw_arg")"
        
        if [[ "$arg" == --* ]] || [[ "$arg" == -* && ${#arg} -eq 2 ]]; then
            # This is an option (long or short), add it as-is
            abs_args+=("$arg")
            i=$((i+1))
            # Check if this option has a value
            if [[ $i -lt $# ]]; then
                local raw_next_arg="${@:i+1:1}"
                local next_arg="$(sanitize_arg "$raw_next_arg")"
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
        # run the script - use array expansion for safety
        uv run python "$script_path" "${abs_args[@]}"
    else
        # Check Python version
        check_python_version

        echo "uv not found, using pip..."
        cd "$project_root"
        # Set PYTHONPATH to include project root
        export PYTHONPATH="$project_root:$PYTHONPATH"
        pip install -r requirements.txt
        # run the script - use array expansion for safety
        python "$script_path" "${abs_args[@]}"
    fi
}