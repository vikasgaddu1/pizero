#!/usr/bin/env python3
"""
Environment Check Script
Verifies that all required packages are installed
Run this FIRST before running the simulation or deploying
"""

import sys
import subprocess

print("="*60)
print("AI Vision Assistant - Environment Check")
print("="*60)
print()

# Check Python version
print("Python Version Check:")
py_version = sys.version_info
print(f"  Current: Python {py_version.major}.{py_version.minor}.{py_version.micro}")

if py_version.major < 3 or (py_version.major == 3 and py_version.minor < 7):
    print("  ✗ Python 3.7+ required")
    print("  Please upgrade Python")
    sys.exit(1)
else:
    print("  ✓ Version OK")

print()

# Required packages for simulation (don't need hardware packages)
simulation_packages = [
    ('PIL', 'Pillow', 'Image processing'),
    ('google.generativeai', 'google-generativeai', 'Gemini API client'),
    ('dotenv', 'python-dotenv', 'Environment variables'),
]

# Optional packages (only needed on Raspberry Pi)
hardware_packages = [
    ('picamera2', 'python3-picamera2', 'Raspberry Pi Camera (Pi only)'),
    ('pyaudio', 'python3-pyaudio', 'Audio input (Pi only)'),
    ('pyttsx3', 'pyttsx3', 'Text-to-speech (Pi only)'),
    ('speech_recognition', 'SpeechRecognition', 'Voice recognition (Pi only)'),
]

print("Required Packages for Simulation:")
print("-" * 60)

missing_packages = []
for module_name, package_name, description in simulation_packages:
    try:
        __import__(module_name.split('.')[0])
        print(f"  ✓ {package_name:.<40} {description}")
    except ImportError:
        print(f"  ✗ {package_name:.<40} MISSING")
        missing_packages.append(package_name)

print()
print("Optional Packages (for Raspberry Pi hardware):")
print("-" * 60)

for module_name, package_name, description in hardware_packages:
    try:
        __import__(module_name.split('.')[0])
        print(f"  ✓ {package_name:.<40} {description}")
    except ImportError:
        print(f"  ○ {package_name:.<40} Not installed (OK for simulation)")

print()
print("="*60)

if missing_packages:
    print("✗ MISSING REQUIRED PACKAGES")
    print("="*60)
    print()
    print("Install missing packages with:")
    print()
    print("  pip3 install " + " ".join(missing_packages))
    print()
    print("Or install all at once:")
    print()
    print("  pip3 install -r requirements.txt")
    print()
    sys.exit(1)
else:
    print("✓ ALL REQUIRED PACKAGES INSTALLED")
    print("="*60)
    print()
    print("You can now:")
    print("  1. Run validation: python3 validate_code.py")
    print("  2. Run simulation: python3 test_simulation.py")
    print()
    print("For Raspberry Pi deployment:")
    print("  - Copy all files to Pi")
    print("  - Run: ./setup.sh")
    print("  - This will install hardware packages")
    print()
    sys.exit(0)
