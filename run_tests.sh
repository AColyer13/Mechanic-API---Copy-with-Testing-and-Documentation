#!/bin/bash
# Test execution script for Mechanic Shop API
# Uses unittest discover to run all tests in the tests directory
# This ensures reproducible test execution for graders and CI systems

echo "========================================"
echo "Mechanic Shop API - Test Suite"
echo "========================================"
echo ""

# Activate virtual environment if not already active
if [ -z "$VIRTUAL_ENV" ]; then
    echo "Activating virtual environment..."
    source .venv/Scripts/activate || source .venv/bin/activate
    if [ $? -ne 0 ]; then
        echo "ERROR: Failed to activate virtual environment"
        echo "Please ensure .venv exists and is properly configured"
        exit 1
    fi
fi

echo "Running tests with unittest discover..."
echo ""

# Run unittest discover with verbose output
python -m unittest discover tests -v

# Capture exit code
TEST_EXIT_CODE=$?

echo ""
echo "========================================"
if [ $TEST_EXIT_CODE -eq 0 ]; then
    echo "All tests passed successfully!"
else
    echo "Some tests failed. Please review the output above."
fi
echo "========================================"

exit $TEST_EXIT_CODE
