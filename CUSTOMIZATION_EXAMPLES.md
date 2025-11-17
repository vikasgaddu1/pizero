# Configuration Examples and Customization Guide

This document provides examples of how to customize the AI Vision Assistant for different use cases.

## Basic Configuration Options

All configuration is in the `Config` class in `main.py`. Here are the main settings:

```python
class Config:
    # API Settings
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    GEMINI_MODEL = 'gemini-1.5-flash'
    
    # Image Settings
    MAX_IMAGE_SIZE = 1024
    JPEG_QUALITY = 85
    IMAGE_DIR = 'captured_images'
    
    # Camera Settings
    CAMERA_RESOLUTION = (1920, 1080)
    CAMERA_WARMUP_TIME = 2
    
    # Voice Recognition Settings
    KEYWORD = 'click'
    EXIT_KEYWORDS = ['exit', 'quit', 'stop']
    MICROPHONE_INDEX = None
    
    # Text-to-Speech Settings
    TTS_RATE = 150
    TTS_VOLUME = 0.9
```

---

## Dynamic Voice Prompts (NEW!)

The system now supports custom voice requests! Instead of just saying "click", you can tell the AI what you want:

### How It Works
The AI analyzes your spoken request and tailors its response:

```
User says: "click read the prescription"
→ AI focuses on medication info: name, dosage, warnings, expiration

User says: "click what ingredients are in this"
→ AI focuses on food ingredients, allergens, nutrition info

User says: "click read this document"
→ AI extracts and reads text from the document

User says: "click what is this"
→ AI provides a general description and context
```

### Supported Request Types

**Medication/Prescription Keywords:**
- prescription, medication, medicine, pill, drug, dosage, dose

**Food/Nutrition Keywords:**
- food, ingredients, nutrition, allergen, eat, calories

**Document/Text Keywords:**
- read, document, letter, text, form, paper

**General Keywords:**
- what, identify, describe, tell me

### Example Voice Commands

| What You Say | What AI Does |
|--------------|--------------|
| "click" | Auto-detects content type and provides relevant info |
| "click read the prescription to me" | Reads medication label with dosage and warnings |
| "click what's the dosage" | Focuses specifically on dosage information |
| "click check for allergens" | Looks for allergen warnings on food labels |
| "click what ingredients are in this" | Lists food ingredients |
| "click read this letter" | Extracts and reads text from documents |
| "click what is this object" | Provides general description |

### No Code Changes Needed!
The dynamic prompt system works out of the box. Just speak naturally and tell the AI what you need!

---

## Use Case Examples

### 1. Security Camera Mode

**Goal:** Quick captures with timestamp logging

```python
class Config:
    # Faster, lower quality for rapid captures
    MAX_IMAGE_SIZE = 640
    JPEG_QUALITY = 70
    CAMERA_RESOLUTION = (1280, 720)
    
    # Multiple trigger keywords
    KEYWORD = 'capture'  # or 'security', 'intruder'
    
    # Save with detailed timestamps
    IMAGE_DIR = 'security_logs'
```

**Additional modification in `capture_image` method:**
```python
def capture_image(self):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    filepath = os.path.join(self.config.IMAGE_DIR, f"security_{timestamp}.jpg")
    # ... rest of code
```

### 2. High-Quality Photo Documentation

**Goal:** Best quality images for detailed analysis

```python
class Config:
    # Maximum quality
    MAX_IMAGE_SIZE = 2048
    JPEG_QUALITY = 95
    CAMERA_RESOLUTION = (2592, 1944)  # Max for Pi Camera V2
    
    # Longer warmup for better exposure
    CAMERA_WARMUP_TIME = 3
    
    # Professional keyword
    KEYWORD = 'photograph'
```

### 3. Education/Learning Tool

**Goal:** Detailed descriptions for learning

```python
class Config:
    # Good balance of quality and speed
    MAX_IMAGE_SIZE = 1280
    JPEG_QUALITY = 85
    
    # Child-friendly keyword
    KEYWORD = 'what is this'  # or 'tell me', 'explain'
    
    # Slower speech for clarity
    TTS_RATE = 120
    TTS_VOLUME = 1.0
```

**Modify the prompt in `analyze_image` method:**
```python
prompt = """Please describe this image in a way that's educational and easy to understand.
Include:
- What the main object/subject is
- Interesting facts about it
- Colors and shapes you notice
- Any educational context

Make it engaging and informative for learners!"""
```

### 4. Accessibility Assistant

**Goal:** Help visually impaired users understand surroundings

```python
class Config:
    # Fast response time
    MAX_IMAGE_SIZE = 800
    JPEG_QUALITY = 80
    
    # Simple keyword
    KEYWORD = 'see'  # or 'look', 'view'
    
    # Clear, slower speech
    TTS_RATE = 140
    TTS_VOLUME = 1.0
```

**Modify the prompt:**
```python
prompt = """Describe this scene as if helping a visually impaired person navigate.
Focus on:
- Spatial layout (what's where)
- Potential obstacles or hazards
- People present and their actions
- Text visible in the image
- Overall safety of the environment

Be specific about locations (left, right, center, foreground, background)."""
```

### 5. Inventory Management

**Goal:** Quick item identification and logging

```python
class Config:
    # Fast captures
    MAX_IMAGE_SIZE = 800
    JPEG_QUALITY = 75
    
    # Professional keyword
    KEYWORD = 'scan'  # or 'inventory', 'catalog'
    
    # Organized storage
    IMAGE_DIR = 'inventory_scans'
```

**Modify the prompt:**
```python
prompt = """Identify and describe items in this image for inventory purposes.
Provide:
- Item names and types
- Quantities (if countable)
- Condition (new, used, damaged)
- Brand names or labels visible
- Any serial numbers or barcodes visible

Be concise and factual."""
```

**Add CSV logging in `process_capture_command`:**
```python
def process_capture_command(self):
    # ... existing code ...
    
    # Log to CSV
    import csv
    log_file = 'inventory_log.csv'
    with open(log_file, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            datetime.now().isoformat(),
            filepath,
            description[:100]  # First 100 chars
        ])
```

### 6. Plant/Garden Assistant

**Goal:** Identify and care for plants

```python
class Config:
    # Good quality for plant details
    MAX_IMAGE_SIZE = 1280
    JPEG_QUALITY = 88
    
    # Natural keyword
    KEYWORD = 'plant'  # or 'identify', 'flower'
```

**Modify the prompt:**
```python
prompt = """Analyze this plant image and provide:
- Plant type/species (if identifiable)
- Health status (healthy, needs attention, signs of disease)
- Care recommendations (water, light, temperature)
- Growth stage
- Any visible issues (pests, disease, nutrient deficiency)
- Interesting facts about this plant

Be specific and actionable in your recommendations."""
```

### 7. Food/Recipe Assistant

**Goal:** Identify food and suggest recipes

```python
class Config:
    MAX_IMAGE_SIZE = 1024
    JPEG_QUALITY = 85
    
    KEYWORD = 'food'  # or 'recipe', 'cook'
```

**Modify the prompt:**
```python
prompt = """Identify the food items in this image and provide:
- What food/ingredients are visible
- Estimated quantities
- Potential recipes using these ingredients
- Nutritional considerations
- Storage recommendations
- Best before considerations

Be helpful and practical."""
```

---

## Advanced Customizations

### Multiple Keywords with Different Actions

Modify the `run` method:

```python
def run(self):
    KEYWORD_ACTIONS = {
        'click': self.process_capture_command,
        'identify': self.identify_mode,
        'describe': self.detailed_mode,
        'quick': self.quick_mode
    }
    
    while True:
        text = self.listen_for_keyword()
        
        for keyword, action in KEYWORD_ACTIONS.items():
            if keyword in text:
                action()
                break
```

Then add different processing methods:

```python
def detailed_mode(self):
    """Detailed analysis mode"""
    self.speak("Taking detailed picture")
    # Use higher quality settings temporarily
    # ... implementation ...

def quick_mode(self):
    """Quick identification mode"""
    self.speak("Quick scan")
    # Use lower quality for speed
    # ... implementation ...
```

### Save Analysis to File

Add logging to `analyze_image`:

```python
def analyze_image(self, image):
    description = # ... get description ...
    
    # Save to log file
    log_file = 'analysis_log.txt'
    with open(log_file, 'a') as f:
        f.write(f"\n{'='*50}\n")
        f.write(f"Time: {datetime.now().isoformat()}\n")
        f.write(f"Image: {filepath}\n")
        f.write(f"Analysis: {description}\n")
    
    return description
```

### Add LED Status Indicators

If you add LEDs to GPIO pins:

```python
import RPi.GPIO as GPIO

class VisionAssistant:
    def __init__(self, config):
        # ... existing code ...
        
        # Setup LED
        self.LED_PIN = 18
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.LED_PIN, GPIO.OUT)
    
    def process_capture_command(self):
        GPIO.output(self.LED_PIN, GPIO.HIGH)  # LED on
        try:
            # ... processing ...
        finally:
            GPIO.output(self.LED_PIN, GPIO.LOW)  # LED off
```

### Continuous Listening Mode

Add an alternative mode that doesn't require keyword:

```python
def continuous_mode(self):
    """Capture every N seconds"""
    import time
    
    interval = 30  # seconds
    
    while True:
        print(f"Auto-capturing in {interval} seconds...")
        time.sleep(interval)
        self.process_capture_command()
```

### Web Interface

Add Flask for remote control:

```python
from flask import Flask, jsonify, request
import threading

app = Flask(__name__)
assistant = None

@app.route('/capture', methods=['POST'])
def web_capture():
    if assistant:
        threading.Thread(target=assistant.process_capture_command).start()
        return jsonify({"status": "capturing"})
    return jsonify({"error": "Assistant not initialized"}), 500

@app.route('/status', methods=['GET'])
def status():
    return jsonify({"status": "ready"})

def run_web_server():
    app.run(host='0.0.0.0', port=5000)

# In main():
web_thread = threading.Thread(target=run_web_server, daemon=True)
web_thread.start()
```

### Database Storage

Use SQLite to store captures:

```python
import sqlite3

def init_database():
    conn = sqlite3.connect('captures.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS captures
                 (id INTEGER PRIMARY KEY,
                  timestamp TEXT,
                  filepath TEXT,
                  description TEXT)''')
    conn.commit()
    conn.close()

def save_to_database(filepath, description):
    conn = sqlite3.connect('captures.db')
    c = conn.cursor()
    c.execute("INSERT INTO captures (timestamp, filepath, description) VALUES (?, ?, ?)",
              (datetime.now().isoformat(), filepath, description))
    conn.commit()
    conn.close()
```

### Email Notifications

Send captures via email:

```python
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

def email_capture(filepath, description):
    sender = os.getenv('EMAIL_SENDER')
    password = os.getenv('EMAIL_PASSWORD')
    receiver = os.getenv('EMAIL_RECEIVER')
    
    msg = MIMEMultipart()
    msg['Subject'] = f'AI Vision Capture: {datetime.now().strftime("%Y-%m-%d %H:%M")}'
    msg['From'] = sender
    msg['To'] = receiver
    
    msg.attach(MIMEText(description, 'plain'))
    
    with open(filepath, 'rb') as f:
        img = MIMEImage(f.read())
        msg.attach(img)
    
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(sender, password)
        server.send_message(msg)
```

---

## Performance Tuning Guide

### For Pi Zero W (Lower Power)

```python
class Config:
    MAX_IMAGE_SIZE = 640
    JPEG_QUALITY = 75
    CAMERA_RESOLUTION = (1280, 720)
    CAMERA_WARMUP_TIME = 3
```

### For Pi Zero 2 W (Better Performance)

```python
class Config:
    MAX_IMAGE_SIZE = 1280
    JPEG_QUALITY = 85
    CAMERA_RESOLUTION = (1920, 1080)
    CAMERA_WARMUP_TIME = 2
```

### For Pi 4 (Maximum Performance)

```python
class Config:
    MAX_IMAGE_SIZE = 2048
    JPEG_QUALITY = 95
    CAMERA_RESOLUTION = (2592, 1944)
    CAMERA_WARMUP_TIME = 1
```

---

## Testing Configurations

Create a test script to try different settings:

```python
#!/usr/bin/env python3
"""
Test different configurations
"""

configs = [
    {"name": "Fast", "size": 640, "quality": 70},
    {"name": "Balanced", "size": 1024, "quality": 85},
    {"name": "Quality", "size": 1920, "quality": 95}
]

for config in configs:
    print(f"\nTesting {config['name']} mode...")
    print(f"Size: {config['size']}, Quality: {config['quality']}")
    
    # Set config
    MAX_IMAGE_SIZE = config['size']
    JPEG_QUALITY = config['quality']
    
    # Capture and time it
    import time
    start = time.time()
    # ... capture and analyze ...
    elapsed = time.time() - start
    
    print(f"Time: {elapsed:.2f}s")
```

---

## Environment Variables

Add more configuration via .env:

```bash
# .env file
GEMINI_API_KEY=your_key_here
KEYWORD=click
IMAGE_SIZE=1024
JPEG_QUALITY=85
TTS_RATE=150
MICROPHONE_INDEX=0
```

Then in code:

```python
class Config:
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    KEYWORD = os.getenv('KEYWORD', 'click')
    MAX_IMAGE_SIZE = int(os.getenv('IMAGE_SIZE', '1024'))
    JPEG_QUALITY = int(os.getenv('JPEG_QUALITY', '85'))
    TTS_RATE = int(os.getenv('TTS_RATE', '150'))
    MICROPHONE_INDEX = int(os.getenv('MICROPHONE_INDEX')) if os.getenv('MICROPHONE_INDEX') else None
```

---

## Tips for Best Results

### Image Quality
- Good lighting is crucial
- Avoid backlighting
- Keep objects in focus
- Fill frame with subject
- Avoid motion blur

### Voice Recognition
- Speak clearly and naturally
- Reduce background noise
- Consistent volume
- Wait for "Listening" prompt
- Avoid very short or long keywords

### API Usage
- Monitor your quota
- Use appropriate image size
- Cache common queries if possible
- Handle rate limits gracefully

### System Performance
- Close unnecessary services
- Use appropriate resolution
- Monitor temperature (add heatsink)
- Consider power supply quality
- Regular system updates

---

Choose the configuration that best fits your use case and hardware capabilities!
