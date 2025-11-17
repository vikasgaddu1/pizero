# Troubleshooting Guide - AI Vision Assistant

## Quick Diagnostic Steps

Run this command to check all components:
```bash
python3 << 'EOF'
import os
import sys

print("=== System Check ===\n")

# Check Python version
print(f"Python version: {sys.version}")

# Check camera
print("\n--- Camera ---")
os.system("vcgencmd get_camera")

# Check audio
print("\n--- Audio Playback Devices ---")
os.system("aplay -l")

print("\n--- Audio Recording Devices ---")
os.system("arecord -l")

# Check internet
print("\n--- Internet Connection ---")
os.system("ping -c 3 google.com")

# Check .env file
print("\n--- API Configuration ---")
if os.path.exists(".env"):
    print("✓ .env file exists")
    with open(".env") as f:
        content = f.read()
        if "GEMINI_API_KEY" in content and "your_" not in content:
            print("✓ API key configured")
        else:
            print("✗ API key not configured")
else:
    print("✗ .env file missing")

# Check dependencies
print("\n--- Python Packages ---")
packages = ["picamera2", "PIL", "speech_recognition", "pyttsx3", "google.generativeai"]
for pkg in packages:
    try:
        __import__(pkg.replace("-", "_").replace("google.generativeai", "google"))
        print(f"✓ {pkg}")
    except ImportError:
        print(f"✗ {pkg} - NOT INSTALLED")

EOF
```

---

## Problem Categories

1. [Camera Issues](#camera-issues)
2. [Audio Input Issues (Microphone)](#audio-input-issues)
3. [Audio Output Issues (Speaker)](#audio-output-issues)
4. [API and Internet Issues](#api-and-internet-issues)
5. [Performance Issues](#performance-issues)
6. [Python Errors](#python-errors)

---

## Camera Issues

### Camera Not Detected

**Symptoms:**
- Error: "Camera is not enabled"
- `vcgencmd get_camera` shows `supported=0 detected=0`

**Solutions:**

1. **Enable camera in config:**
```bash
sudo raspi-config
# Navigate to: Interface Options → Camera → Enable
sudo reboot
```

2. **Check ribbon cable:**
- Power off Pi completely
- Ensure ribbon cable is fully inserted
- Blue side should face the Ethernet port side
- Reconnect and power on

3. **Verify detection:**
```bash
vcgencmd get_camera
# Should show: supported=1 detected=1
```

### Camera Module Not Found

**Symptoms:**
- Error: "No module named 'picamera2'"

**Solution:**
```bash
sudo apt-get install -y python3-picamera2
pip3 install --break-system-packages picamera2
```

### Camera Timeout or Freeze

**Symptoms:**
- Program hangs when capturing
- Timeout errors

**Solutions:**

1. **Increase warmup time:**
Edit `main.py`, line with `CAMERA_WARMUP_TIME`:
```python
CAMERA_WARMUP_TIME = 3  # Increase from 2 to 3 seconds
```

2. **Test camera standalone:**
```bash
libcamera-hello --timeout 5000
libcamera-still -o test.jpg
```

3. **Check system resources:**
```bash
free -h
# If low memory, close other applications
```

### Poor Image Quality

**Solutions:**

1. **Adjust focus:** If using adjustable lens, manually focus

2. **Improve lighting:** Add more light to scene

3. **Increase resolution:**
Edit `main.py`:
```python
CAMERA_RESOLUTION = (2592, 1944)  # Max for Pi Camera V2
```

4. **Reduce JPEG compression:**
Edit `main.py`:
```python
JPEG_QUALITY = 95  # Increase from 85 to 95
```

---

## Audio Input Issues

### Microphone Not Working

**Symptoms:**
- "Listening for keyword..." but doesn't hear anything
- "Could not understand audio" repeatedly

**Solutions:**

1. **List available microphones:**
```bash
python3 -c "import speech_recognition as sr; print(sr.Microphone.list_microphone_names())"
```

2. **Test microphone:**
```bash
# Record 5 seconds
arecord -D plughw:1,0 -d 5 test.wav

# If that fails, try default:
arecord -d 5 test.wav

# Play back
aplay test.wav
```

3. **Check microphone levels:**
```bash
alsamixer
# Use arrow keys to navigate to microphone
# Press 'M' to unmute if needed
# Use up arrow to increase level
```

4. **Specify microphone index:**
If you have multiple microphones, edit `main.py`:
```python
MICROPHONE_INDEX = 1  # Change from None to specific index
```

### Speech Recognition Not Working

**Symptoms:**
- Microphone works but words aren't recognized
- "Could not understand audio"

**Solutions:**

1. **Check internet connection:**
```bash
ping -c 3 google.com
# Speech recognition requires internet
```

2. **Speak more clearly:**
- Speak louder and clearer
- Reduce background noise
- Speak closer to microphone

3. **Adjust recognition settings:**
Edit `main.py`, in `listen_for_keyword` method:
```python
# Increase phrase time limit
audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=5)

# Adjust ambient noise duration
self.recognizer.adjust_for_ambient_noise(source, duration=1.0)
```

4. **Test with different words:**
The keyword "click" might not be recognized clearly. Try changing:
```python
KEYWORD = 'picture'  # or 'capture', 'photo'
```

### PyAudio Errors

**Symptoms:**
- Error: "No module named '_portaudio'"
- Error: "PortAudio library not found"

**Solutions:**
```bash
sudo apt-get install portaudio19-dev python3-pyaudio
pip3 install --break-system-packages pyaudio
```

---

## Audio Output Issues

### No Sound from Speaker

**Symptoms:**
- Program runs but no audio output
- TTS should speak but doesn't

**Solutions:**

1. **Check speaker connection:**
- Verify speaker is plugged into Audio DAC Hat
- Check power to speaker if it's powered

2. **Test audio output:**
```bash
speaker-test -t wav -c 2
# You should hear "Front Left" and "Front Right"
```

3. **Check volume:**
```bash
alsamixer
# Increase volume using up arrow
# Ensure not muted (no 'MM' shown)
```

4. **Select correct audio device:**
```bash
# List devices
aplay -l

# Set default device
sudo nano /etc/asound.conf

# Add:
defaults.pcm.card 1
defaults.ctl.card 1
```

5. **Test with simple sound:**
```bash
echo "Testing audio" | espeak
```

### TTS Voice Quality Issues

**Solutions:**

1. **Adjust TTS settings:**
Edit `main.py`:
```python
TTS_RATE = 130  # Slower speech
TTS_VOLUME = 1.0  # Maximum volume
```

2. **Try different TTS engine:**
```python
# In _setup_tts method
voices = self.tts_engine.getProperty('voices')
self.tts_engine.setProperty('voice', voices[1].id)  # Try different voice
```

---

## API and Internet Issues

### "GEMINI_API_KEY not found"

**Solutions:**

1. **Verify .env file exists:**
```bash
ls -la .env
cat .env
```

2. **Check file content:**
```bash
cat .env
# Should contain:
# GEMINI_API_KEY=your_actual_key_here
```

3. **No spaces around equals sign:**
```
# WRONG
GEMINI_API_KEY = your_key

# CORRECT
GEMINI_API_KEY=your_key
```

4. **Get new API key:**
Visit: https://makersuite.google.com/app/apikey

### API Rate Limit Errors

**Symptoms:**
- Error: "429 Too Many Requests"
- Error: "Quota exceeded"

**Solutions:**

1. **Wait and retry:**
Free tier: 60 requests per minute

2. **Check quota:**
Visit: https://console.cloud.google.com

3. **Add delay between requests:**
Edit `main.py`, in `run` method:
```python
if self.config.KEYWORD in text:
    time.sleep(2)  # Add 2 second delay
    self.process_capture_command()
```

### Network Connection Issues

**Symptoms:**
- Error: "Failed to connect to API"
- Timeout errors

**Solutions:**

1. **Check WiFi connection:**
```bash
iwconfig
ping -c 3 google.com
```

2. **Restart network:**
```bash
sudo systemctl restart networking
```

3. **Check DNS:**
```bash
cat /etc/resolv.conf
# Should contain nameserver entries
```

### SSL Certificate Errors

**Solution:**
```bash
sudo apt-get install ca-certificates
sudo update-ca-certificates
```

---

## Performance Issues

### Slow Image Analysis

**Symptoms:**
- Analysis takes >10 seconds
- System feels sluggish

**Solutions:**

1. **Reduce image size:**
Edit `main.py`:
```python
MAX_IMAGE_SIZE = 768  # Reduce from 1024
JPEG_QUALITY = 75  # Reduce from 85
CAMERA_RESOLUTION = (1280, 720)  # Reduce from (1920, 1080)
```

2. **Use Pi Zero 2 W:**
- Much faster processor
- Better for this application

3. **Close other applications:**
```bash
# Check what's running
htop

# Free memory
sudo systemctl stop unnecessary-services
```

4. **Add swap space:**
```bash
sudo dphys-swapfile swapoff
sudo nano /etc/dphys-swapfile
# Change: CONF_SWAPSIZE=1024
sudo dphys-swapfile setup
sudo dphys-swapfile swapon
```

### Memory Errors

**Symptoms:**
- Error: "Out of memory"
- System crash during analysis

**Solutions:**

1. **Reduce image size** (see above)

2. **Close other applications:**
```bash
sudo systemctl stop bluetooth
sudo systemctl stop cups
```

3. **Monitor memory:**
```bash
free -h
```

---

## Python Errors

### ModuleNotFoundError

**Error:** `No module named 'xyz'`

**Solution:**
```bash
pip3 install --break-system-packages xyz
```

### Permission Denied Errors

**Solutions:**

1. **Camera permission:**
```bash
sudo usermod -a -G video $USER
# Logout and login again
```

2. **File permission:**
```bash
chmod +x setup.sh
chmod +x main.py
```

### ImportError: cannot import name

**Solution:**
```bash
# Reinstall package
pip3 uninstall package-name
pip3 install --break-system-packages package-name
```

---

## Getting More Help

### Enable Debug Mode

Edit `main.py`, add at top:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Generate Debug Log

```bash
python3 main.py 2>&1 | tee debug.log
# Send debug.log when asking for help
```

### Check System Logs

```bash
# Recent errors
sudo journalctl -xe

# Program logs if running as service
sudo journalctl -u vision-assistant.service -f
```

### Test Each Component

Create `test_components.py`:
```python
#!/usr/bin/env python3
import sys

print("Testing components...\n")

# Test 1: Camera
print("1. Testing camera...")
try:
    from picamera2 import Picamera2
    camera = Picamera2()
    print("   ✓ Camera module imported")
    camera.start()
    camera.stop()
    print("   ✓ Camera initialized")
except Exception as e:
    print(f"   ✗ Camera error: {e}")

# Test 2: Speech Recognition
print("\n2. Testing speech recognition...")
try:
    import speech_recognition as sr
    r = sr.Recognizer()
    print("   ✓ Speech recognition imported")
    with sr.Microphone() as source:
        print("   ✓ Microphone detected")
except Exception as e:
    print(f"   ✗ Speech recognition error: {e}")

# Test 3: TTS
print("\n3. Testing text-to-speech...")
try:
    import pyttsx3
    engine = pyttsx3.init()
    print("   ✓ TTS initialized")
except Exception as e:
    print(f"   ✗ TTS error: {e}")

# Test 4: Gemini API
print("\n4. Testing Gemini API...")
try:
    import google.generativeai as genai
    from dotenv import load_dotenv
    import os
    load_dotenv()
    api_key = os.getenv('GEMINI_API_KEY')
    if api_key and 'your_' not in api_key:
        print("   ✓ API key configured")
    else:
        print("   ✗ API key not configured")
except Exception as e:
    print(f"   ✗ API error: {e}")

print("\nTest complete!")
```

Run with:
```bash
python3 test_components.py
```

---

## Still Having Issues?

1. **Reboot the Pi:**
```bash
sudo reboot
```

2. **Fresh install:**
```bash
cd ~/ai-vision-assistant
./setup.sh
```

3. **Check project documentation:**
- PROJECT_README.md
- QUICK_START.md

4. **Online resources:**
- Gemini API: https://ai.google.dev/docs
- Raspberry Pi Forums: https://forums.raspberrypi.com
- RASPIAUDIO Support: https://raspiaudio.com/support

---

**Remember:** Most issues are solved by:
1. Checking connections
2. Verifying API key
3. Ensuring internet connection
4. Rebooting after changes
