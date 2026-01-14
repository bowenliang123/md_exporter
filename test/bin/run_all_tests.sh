#!/bin/bash

# Run all test scripts in test/bin

# Source common functions
. "$(dirname "${BASH_SOURCE[0]}")/test_common.sh"

# Set up test environment
setup_test_env

# Run all test scripts
passed=0
failed=0

echo "Running all test scripts..."
echo "=================================="

for test_script in "$(dirname "${BASH_SOURCE[0]}")"/test_*.sh; do
    if [ "$test_script" != "$(dirname "${BASH_SOURCE[0]}")/run_all_tests.sh" ]; then
        "$test_script"
        if [ $? -eq 0 ]; then
            passed=$((passed + 1))
        else
            failed=$((failed + 1))
        fi
        echo "=================================="
    fi
done

echo "Test Results:"
echo "Passed: $passed"
echo "Failed: $failed"
echo "Total: $((passed + failed))"

if [ $failed -eq 0 ]; then
    echo "✓ All tests passed!"
    exit 0
else
    echo "✗ Some tests failed!"
    exit 1
fi