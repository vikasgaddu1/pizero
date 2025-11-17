#!/bin/bash

# AI Vision Assistant Setup Script for Raspberry Pi Zero
# This script installs all necessary dependencies and configures the system

set -e

echo "================================================"
echo "AI Vision Assistant - Installation Script"
echo "================================================"
echo ""

# Check if running on Raspberry Pi
if ! grep -q "Raspberry Pi" /proc/cpuinfo; then
    echo "Warning: This script is designed for Raspberry Pi"
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Update system
echo "Step 1: Updating system packages..."
sudo apt-get update

# Install system dependencies
echo "Step 2: Installing system dependencies..."
sudo apt-get install -y \
    python3-pip \
    python3-picamera2 \
    portaudio19-dev \
    python3-pyaudio \
    flac \
    espeak \
    alsa-utils \
    python3-dev \
    python3-setuptools

# Install Python packages
echo "Step 3: Installing Python packages..."
pip3 install --break-system-packages -r requirements.txt

# Enable camera interface
echo "Step 4: Enabling camera interface..."
sudo raspi-config nonint do_camera 0

# Create image directory
echo "Step 5: Creating image directory..."
mkdir -p captured_images

# Check for .env file
if [ ! -f .env ]; then
    echo ""
    echo "Step 6: Setting up .env file..."
    cp .env.example .env
    echo "Please edit .env file and add your Gemini API key"
    echo "Get your key from: https://makersuite.google.com/app/apikey"
    echo ""
    read -p "Press Enter to edit .env file now..."
    nano .env
fi

# Test audio devices
echo ""
echo "Step 7: Testing audio devices..."
echo "Available playback devices:"
aplay -l
echo ""
echo "Available recording devices:"
arecord -l
echo ""

# Test microphone
echo "Testing microphone (speak for 3 seconds)..."
arecord -D plughw:1,0 -d 3 -f cd test.wav 2>/dev/null || \
arecord -d 3 -f cd test.wav
echo "Playing back recording..."
aplay test.wav
rm -f test.wav

# Final instructions
echo ""
echo "================================================"
echo "Installation Complete!"
echo "================================================"
echo ""
echo "To run the program:"
echo "  python3 main.py"
echo ""
echo "Make sure you have:"
echo "  1. Added your Gemini API key to .env file"
echo "  2. Connected your Pi Camera"
echo "  3. Connected your RASPIAUDIO DAC Hat"
echo "  4. Connected speaker and microphone"
echo ""
echo "Troubleshooting:"
echo "  - If camera doesn't work: sudo reboot"
echo "  - If audio doesn't work: check alsamixer settings"
echo "  - If speech recognition fails: check internet connection"
echo ""
echo "================================================"
