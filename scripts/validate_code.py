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

# Find all Python files in the package
root_dir = Path(__file__).parent.parent
package_dir = root_dir / 'pizero'
tests_dir = root_dir / 'tests'
scripts_dir = root_dir / 'scripts'

python_files = []
# Add package files
if package_dir.exists():
    python_files.extend(package_dir.glob('*.py'))
# Add test files
if tests_dir.exists():
    python_files.extend(tests_dir.glob('*.py'))
# Add script files
if scripts_dir.exists():
    python_files.extend(scripts_dir.glob('*.py'))
# Add main.py if it exists
main_py = root_dir / 'main.py'
if main_py.exists():
    python_files.append(main_py)

all_valid = True
errors_found = []

print("Validating Python files...\n")

for filepath in python_files:
    try:
        # Compile the file
        py_compile.compile(str(filepath), doraise=True)

        # Check file size
        size_kb = filepath.stat().st_size / 1024

        # Count lines
        with open(filepath, 'r') as f:
            lines = len(f.readlines())

        # Get relative path for display
        rel_path = filepath.relative_to(root_dir)
        print(f"✓ {str(rel_path):.<45} VALID")
        print(f"  └─ {lines} lines, {size_kb:.1f} KB")

    except py_compile.PyCompileError as e:
        all_valid = False
        error_msg = str(e)
        rel_path = filepath.relative_to(root_dir)
        errors_found.append((str(rel_path), error_msg))
        print(f"✗ {str(rel_path):.<45} SYNTAX ERROR")
        print(f"  └─ {error_msg}")

print()
print("="*60)

if all_valid:
    print("✓ ALL FILES VALID - Code is ready to deploy!")
    print("="*60)
    print()
    print("Next steps:")
    print("1. Run simulation test: python3 tests/test_simulation.py")
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
