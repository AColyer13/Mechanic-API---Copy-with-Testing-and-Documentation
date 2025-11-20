@echo off
REM Test execution script for Mechanic Shop API
REM Uses unittest discover to run all tests in the tests directory
REM This ensures reproducible test execution for graders and CI systems

echo ========================================
echo Mechanic Shop API - Test Suite
echo ========================================
echo.

REM Activate virtual environment if not already active
if not defined VIRTUAL_ENV (
    echo Activating virtual environment...
    call .venv\Scripts\activate.bat
    if errorlevel 1 (
        echo ERROR: Failed to activate virtual environment
        echo Please ensure .venv exists and is properly configured
        exit /b 1
    )
)

echo Running tests with unittest discover...
echo.

REM Run unittest discover with verbose output
.venv\Scripts\python.exe -m unittest discover tests -v

REM Capture exit code
set TEST_EXIT_CODE=%errorlevel%

echo.
echo ========================================
if %TEST_EXIT_CODE% equ 0 (
    echo All tests passed successfully!
) else (
    echo Some tests failed. Please review the output above.
)
echo ========================================

exit /b %TEST_EXIT_CODE%
