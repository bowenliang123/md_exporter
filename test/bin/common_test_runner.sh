#!/bin/bash

# Common functions for test scripts

# Set up test environment
function setup_test_env() {
    TEST_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    PROJECT_ROOT="$(dirname "$(dirname "$TEST_DIR")")"
    OUTPUT_DIR="$PROJECT_ROOT/test_output"
    
    # Create output directory if it doesn't exist
    mkdir -p "$OUTPUT_DIR"
    
    echo "TEST_DIR: $TEST_DIR"
    echo "PROJECT_ROOT: $PROJECT_ROOT"
    echo "OUTPUT_DIR: $OUTPUT_DIR"
}

# Clean up test output
function cleanup_test_output() {
    local output_path="$1"
    if [ -f "$output_path" ]; then
        rm -f "$output_path"
    elif [ -d "$output_path" ]; then
        rm -rf "$output_path"
    fi
}

# Verify file output
function verify_file_output() {
    local output_file="$1"
    if [ -f "$output_file" ] && [ -s "$output_file" ]; then
        return 0
    else
        return 1
    fi
}

# Verify directory output
function verify_dir_output() {
    local output_dir="$1"
    if [ -d "$output_dir" ] && [ $(ls -1 "$output_dir" | wc -l) -gt 0 ]; then
        return 0
    else
        return 1
    fi
}

# Verify stdout output
function verify_stdout_output() {
    local output="$1"
    if [ -n "$output" ]; then
        return 0
    else
        return 1
    fi
}

# Run test for file output script
function run_file_test() {
    local script_name="$1"
    local input_file="$2"
    local output_ext="$3"
    
    local output_file="$OUTPUT_DIR/test_${script_name}.${output_ext}"
    
    # Clean up previous test output
    cleanup_test_output "$output_file"
    
    # Run the bash script
    echo "Running test for ${script_name}..."
    "$PROJECT_ROOT/scripts/md-exporter" "$script_name" "$input_file" "$output_file"
    
    # Verify the output
    if [ $? -eq 0 ] && verify_file_output "$output_file"; then
        echo "✓ Test passed: ${script_name} generated valid output"
        # Clean up test output
        cleanup_test_output "$output_file"
        return 0
    else
        echo "✗ Test failed: ${script_name} did not generate valid output"
        if [ -f "$output_file" ]; then
            echo "Output file exists but is empty or invalid"
            # Clean up test output
            cleanup_test_output "$output_file"
        fi
        return 1
    fi
}

# Run test for directory output script
function run_dir_test() {
    local script_name="$1"
    local input_file="$2"
    
    local output_dir="$OUTPUT_DIR/${script_name}_output"
    
    # Clean up previous test output
    cleanup_test_output "$output_dir"
    
    # Run the bash script
    echo "Running test for ${script_name}..."
    "$PROJECT_ROOT/scripts/md-exporter" "$script_name" "$input_file" "$output_dir"
    
    # Verify the output
    if [ $? -eq 0 ] && verify_dir_output "$output_dir"; then
        echo "✓ Test passed: ${script_name} generated valid output"
        # Clean up test output
        cleanup_test_output "$output_dir"
        return 0
    else
        echo "✗ Test failed: ${script_name} did not generate valid output"
        if [ -d "$output_dir" ]; then
            echo "Output directory exists but is empty"
            # Clean up test output
            cleanup_test_output "$output_dir"
        fi
        return 1
    fi
}

# Run test for stdout output script
function run_stdout_test() {
    local script_name="$1"
    local input_file="$2"
    
    # Run the bash script and capture output
    echo "Running test for ${script_name}..."
    local output="$($PROJECT_ROOT/scripts/md-exporter "$script_name" "$input_file")"
    
    # Verify the output
    if [ $? -eq 0 ] && verify_stdout_output "$output"; then
        echo "✓ Test passed: ${script_name} generated valid output"
        return 0
    else
        echo "✗ Test failed: ${script_name} did not generate valid output"
        return 1
    fi
}