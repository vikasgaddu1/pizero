# Quick Start Guide - AI Vision Assistant

## Prerequisites Checklist
- [ ] Raspberry Pi Zero W (or Pi Zero 2 W)
- [ ] Pi Camera Module connected
- [ ] RASPIAUDIO Audio DAC Hat installed
- [ ] Speaker connected to DAC
- [ ] Microphone connected (or USB mic)
- [ ] Internet connection (WiFi)
- [ ] Gemini API key obtained

## Installation (5 minutes)

### 1. Download Project Files
```bash
cd ~
mkdir ai-vision-assistant
cd ai-vision-assistant
# Copy all project files here
```

### 2. Run Setup Script
```bash
chmod +x setup.sh
./setup.sh
```

The script will:
- Install all dependencies
- Enable camera
- Create necessary directories
- Help you configure API key

### 3. Configure API Key
Edit the `.env` file:
```bash
nano .env
```

Add your Gemini API key:
```
GEMINI_API_KEY=your_actual_api_key_here
```

Get your key from: https://makersuite.google.com/app/apikey

Save and exit (Ctrl+X, then Y, then Enter)

### 4. Reboot (Required for camera)
```bash
sudo reboot
```

## First Run

### 1. Navigate to Project
```bash
cd ~/ai-vision-assistant
```

### 2. Start the Program
```bash
python3 main.py
```

### 3. Wait for Ready Message
You'll hear: "AI Vision Assistant ready"

### 4. Test It!
Say: **"click"**

The system will:
1. Say "Taking picture"
2. Capture an image
3. Say "Analyzing"
4. Describe what it sees

## Usage Tips

### Voice Commands
| Command | Action |
|---------|--------|
| "click" | Capture and auto-analyze image |
| "click read the prescription" | Focus on medication label |
| "click what ingredients" | Focus on food/ingredients |
| "click read this document" | Focus on text reading |
| "click what is this" | General description |
| "exit" or "quit" | Stop the program |

**Pro Tip**: You can add custom requests after "click" to tell the AI what you want to focus on!

### Best Practices
- **Speak clearly** and at normal volume
- Wait for **"Listening for keyword..."** message before speaking
- Ensure good **lighting** for better image analysis
- Keep objects **in focus** and well-framed
- Wait for analysis to complete before next capture

### Optimal Environment
- **Quiet room** for better voice recognition
- **Good lighting** for image quality
- **Stable position** for camera
- **Clear view** of subject

## Common First-Run Issues

### Camera Not Working
```bash
# Check camera detection
vcgencmd get_camera

# Should show: supported=1 detected=1
# If not, check cable connection and reboot
```

### Microphone Not Detected
```bash
# List microphones
python3 -c "import speech_recognition as sr; print(sr.Microphone.list_microphone_names())"

# If empty, check USB mic connection or DAC mic input
```

### API Error
```bash
# Verify .env file exists and contains key
cat .env

# Test internet connection
ping -c 3 google.com
```

### No Audio Output
```bash
# Check volume
alsamixer

# Test speaker
speaker-test -t wav -c 2
```

## Running at Startup (Optional)

To run automatically on boot:

### 1. Create Systemd Service
```bash
sudo nano /etc/systemd/system/vision-assistant.service
```

### 2. Add Configuration
```ini
[Unit]
Description=AI Vision Assistant
After=network-online.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/ai-vision-assistant
ExecStart=/usr/bin/python3 /home/pi/ai-vision-assistant/main.py
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### 3. Enable Service
```bash
sudo systemctl daemon-reload
sudo systemctl enable vision-assistant.service
sudo systemctl start vision-assistant.service
```

### 4. Check Status
```bash
sudo systemctl status vision-assistant.service
```

## Performance Notes

### Pi Zero W
- Works but may be slower
- ~5-10 seconds for analysis
- Consider lower resolution if needed

### Pi Zero 2 W (Recommended)
- Much better performance
- ~3-5 seconds for analysis
- Can handle full resolution

### Optimization Tips
- Lower `MAX_IMAGE_SIZE` in main.py for faster uploads
- Reduce `CAMERA_RESOLUTION` if needed
- Use wired ethernet adapter for stable connection

## What's Next?

### Experiment With:
- Different lighting conditions
- Various objects and scenes
- Different distances from camera
- Indoor vs outdoor scenes

### Customize:
- Change keyword in `Config.KEYWORD`
- Adjust image quality in `Config.JPEG_QUALITY`
- Modify camera resolution in `Config.CAMERA_RESOLUTION`
- Tweak TTS speed in `Config.TTS_RATE`

### Advanced Usage:
- Add multiple keywords for different actions
- Save descriptions to log file
- Add LED indicators for status
- Create web interface
- Implement continuous mode

## Getting Help

### Check Logs
```bash
# Run with verbose output
python3 main.py 2>&1 | tee debug.log
```

### Test Components Individually

**Camera:**
```bash
libcamera-hello
libcamera-still -o test.jpg
```

**Microphone:**
```bash
arecord -d 5 test.wav
aplay test.wav
```

**Speaker:**
```bash
speaker-test -t wav -c 2
```

**Internet:**
```bash
ping -c 3 google.com
```

### Resources
- Gemini API Docs: https://ai.google.dev/docs
- Pi Camera Guide: https://www.raspberrypi.com/documentation/accessories/camera.html
- RASPIAUDIO Support: https://raspiaudio.com

## Success!

If everything works, you should be able to:
1. Say "click"
2. Hear the shutter click
3. Wait a few seconds
4. Hear AI describe what it saw

Congratulations! Your AI Vision Assistant is working! 🎉

---

For detailed documentation, see PROJECT_README.md
For troubleshooting, see TROUBLESHOOTING.md
