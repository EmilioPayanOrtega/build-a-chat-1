import pytest
import sys
import os
import argparse
import subprocess

def run_unit_tests():
    print("\n=== Running Unit Tests ===")
    return pytest.main(["tests"])

def run_e2e_tests():
    print("\n=== Running End-to-End Verification ===")
    # Execute the verification script as a subprocess to ensure clean environment
    script_path = os.path.join(os.path.dirname(__file__), 'scripts', 'verify_full_flow.py')
    result = subprocess.run([sys.executable, script_path])
    return result.returncode

if __name__ == "__main__":
    # Add the current directory to sys.path
    sys.path.append(os.path.abspath(os.path.dirname(__file__)))
    
    parser = argparse.ArgumentParser(description="Run backend tests")
    parser.add_argument('--unit', action='store_true', help="Run unit tests (default)")
    parser.add_argument('--e2e', action='store_true', help="Run end-to-end verification script")
    parser.add_argument('--all', action='store_true', help="Run both unit and e2e tests")
    
    args = parser.parse_args()
    
    # Default to unit tests if no args provided
    if not (args.e2e or args.all):
        args.unit = True
        
    exit_code = 0
    
    if args.unit or args.all:
        exit_code += run_unit_tests()
        
    if args.e2e or args.all:
        if exit_code == 0: # Only run E2E if unit tests passed (or if only E2E requested)
            exit_code += run_e2e_tests()
            
    sys.exit(exit_code)
