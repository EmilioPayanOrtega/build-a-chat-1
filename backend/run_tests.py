import pytest
import sys
import os

if __name__ == "__main__":
    # Add the current directory to sys.path so 'app' can be imported
    sys.path.append(os.path.abspath(os.path.dirname(__file__)))
    
    print("Running tests...")
    # Run pytest on the tests directory
    result = pytest.main(["tests"])
    sys.exit(result)
