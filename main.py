#!/usr/bin/env python3
"""
Subdomain Finder - Main Entry Point
A tool for discovering subdomains of a given domain.
"""

import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    from src.gui import main
except ImportError as e:
    print(f"Error importing modules: {e}")
    print("Please ensure all required dependencies are installed:")
    print("pip install PyQt5 requests")
    sys.exit(1)

if __name__ == "__main__":
    main() 