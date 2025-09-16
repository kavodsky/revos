#!/usr/bin/env python3
"""
Installation script for the Revo library.

This script helps users install the library and its dependencies.
"""

import subprocess
import sys
import os


def run_command(command, description):
    """Run a command and handle errors."""
    print(f"Running: {description}")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✓ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ {description} failed:")
        print(f"  Error: {e.stderr}")
        return False


def main():
    """Main installation function."""
    print("Revo Library Installation")
    print("=" * 30)
    
    # Check Python version
    if sys.version_info < (3, 11):
        print("✗ Python 3.11 or higher is required")
        print(f"  Current version: {sys.version}")
        sys.exit(1)
    
    print(f"✓ Python version: {sys.version.split()[0]}")
    
    # Install the library in development mode
    if not run_command("pip install -e .", "Installing Revo library"):
        print("Installation failed. Please check the error messages above.")
        sys.exit(1)
    
    # Install development dependencies if requested
    if "--dev" in sys.argv:
        if not run_command("pip install -e .[dev]", "Installing development dependencies"):
            print("Development dependencies installation failed.")
            sys.exit(1)
    
    print("\n" + "=" * 30)
    print("Installation completed successfully!")
    print("\nNext steps:")
    print("1. Set your environment variables:")
    print("   export APOLLO_CLIENT_ID='your_client_id'")
    print("   export APOLLO_CLIENT_SECRET='your_client_secret'")
    print("2. Run the example:")
    print("   python examples/basic_usage.py")
    print("3. Run tests:")
    print("   pytest tests/")


if __name__ == "__main__":
    main()
