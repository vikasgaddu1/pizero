#!/usr/bin/env python3
"""
Code Validation Script
Checks that all Python files compile and have no syntax errors
Perfect for pre-deployment validation!
"""

import py_compile
import sys
import os
from pathlib import Path

print("="*60)
print("AI Vision Assistant - Code Validation")
print("="*60)
print()

# Find all Python files
python_files = [
    'main.py',
    'test_simulation.py',
    'validate_code.py'
]

all_valid = True
errors_found = []

print("Validating Python files...\n")

for filename in python_files:
    if not os.path.exists(filename):
        print(f"⚠ {filename:.<45} SKIPPED (not found)")
        continue

    try:
        # Compile the file
        py_compile.compile(filename, doraise=True)

        # Check file size
        size_kb = os.path.getsize(filename) / 1024

        # Count lines
        with open(filename, 'r') as f:
            lines = len(f.readlines())

        print(f"✓ {filename:.<45} VALID")
        print(f"  └─ {lines} lines, {size_kb:.1f} KB")

    except py_compile.PyCompileError as e:
        all_valid = False
        error_msg = str(e)
        errors_found.append((filename, error_msg))
        print(f"✗ {filename:.<45} SYNTAX ERROR")
        print(f"  └─ {error_msg}")

print()
print("="*60)

if all_valid:
    print("✓ ALL FILES VALID - Code is ready to deploy!")
    print("="*60)
    print()
    print("Next steps:")
    print("1. Run simulation test: python3 test_simulation.py")
    print("2. Deploy to Raspberry Pi")
    print("3. Run setup.sh on the Pi")
    print("4. Test with real hardware")
    print()
    sys.exit(0)
else:
    print("✗ ERRORS FOUND - Please fix before deploying")
    print("="*60)
    print()
    print("Errors to fix:")
    for filename, error in errors_found:
        print(f"\n{filename}:")
        print(f"  {error}")
    print()
    sys.exit(1)
