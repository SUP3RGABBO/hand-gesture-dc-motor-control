# Hand Gesture DC Motor Control

Real-time computer vision system that controls DC motor speed using hand gestures detected via webcam.

## Features
- Hand tracking with MediaPipe
- DC motor PWM control
- Serial communication with Arduino
- Real-time gradient speed bar
- LED speed feedback

## Structure
arduino/ → Arduino firmware  
python/ → Computer vision control  
docs/ → circuit photos and diagrams  
media/ → thumbnails and assets  

## Run

pip install -r requirements.txt

python python/main.py
