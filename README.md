# Hand Proximity Prototype
A simple webcam demo that detects a hand, shows a vertical danger line, and highlights DANGER when your hand crosses that line.

# Start Guide
1) Install dependencies:
   pip install -r requirements.txt

2) Run from the project root:
   python -m src.main

   (or) `python src/main.py`

# What you’ll see
- Live camera feed
- Yellow danger line you can drag horizontally
- Hand contour and centroid
- State text: SAFE / WARNING / DANGER
- Big red “DANGER DANGER” overlay while in danger

# Controls
- Drag near the yellow line to move it.

# How it works 
- Skin-mask segmentation (HSV + YCrCb) to find the largest hand contour.
- Ignores the top region to avoid the face.
- Farthest point from the hand centroid is treated as the fingertip.
- If the fingertip crosses the danger line ⇒ DANGER.

# Requirements
- Python 3.8+
- OpenCV
- NumPy