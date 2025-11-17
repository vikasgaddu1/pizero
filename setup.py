#!/usr/bin/env python3
"""
Setup script for AI Vision Assistant package
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text() if readme_file.exists() else ""

# Read requirements
requirements_file = Path(__file__).parent / "requirements.txt"
if requirements_file.exists():
    with open(requirements_file) as f:
        requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]
else:
    requirements = [
        'Pillow>=10.0.0',
        'google-generativeai>=0.3.0',
        'python-dotenv>=1.0.0',
        'SpeechRecognition>=3.10.0',
        'pyttsx3>=2.90',
    ]

# Hardware-specific requirements (only for Raspberry Pi)
raspberry_pi_extras = [
    'picamera2',
    'pyaudio',
]

setup(
    name='pizero-vision-assistant',
    version='1.0.0',
    description='AI Vision Assistant for Raspberry Pi Zero - Voice-controlled image analysis',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Your Name',
    author_email='your.email@example.com',
    url='https://github.com/vikasgaddu1/pizero',
    packages=find_packages(exclude=['tests', 'scripts']),
    include_package_data=True,
    install_requires=requirements,
    extras_require={
        'pi': raspberry_pi_extras,
        'dev': [
            'pytest>=7.0.0',
            'pytest-mock>=3.10.0',
        ],
    },
    entry_points={
        'console_scripts': [
            'pizero-vision=pizero.cli:main',
        ],
    },
    python_requires='>=3.7',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Multimedia :: Graphics :: Capture :: Digital Camera',
    ],
    keywords='raspberry-pi vision ai gemini voice-control accessibility',
    project_urls={
        'Bug Reports': 'https://github.com/vikasgaddu1/pizero/issues',
        'Source': 'https://github.com/vikasgaddu1/pizero',
    },
)
