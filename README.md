# Virtual Mouse Using Hand Gestures

Control your computer's mouse with your hand. A webcam watches your hand, and the program turns finger movements into cursor movement, clicks and scrolling.

## Features

- **Move cursor**: point with your index finger
- **Left click**: touch thumb and index finger (pinch)
- **Right click**: touch index and middle finger
- **Scroll**: move your hand quickly up or down
- **Smooth movement**: reduces cursor jitter
- **Live view**: hand skeleton, active box, FPS and gesture labels
- **Easy settings**: everything is in `config.py`

## Technology Stack

| Part | Tool | What it does |
|------|------|--------------|
| Front-end (visual) | OpenCV | Opens the webcam, shows the live video and draws labels |
| Front-end (visual) | MediaPipe Drawing | Draws the red hand points and lines |
| Back-end (logic) | Python | Main loop and gesture logic |
| Back-end (logic) | MediaPipe Hands | Finds 21 landmarks on your hand |
| Back-end (logic) | PyAutoGUI | Moves the mouse, clicks and scrolls |
| Back-end (logic) | NumPy | Maps camera pixels to screen pixels |

## Requirements

- Windows 10/11
- Python 3.9 to 3.12 (tested with 3.12)
- A webcam

## Installation

```
pip install -r requirements.txt
```

`requirements.txt` pins versions that work together (MediaPipe 0.10.14 is needed because newer versions removed `mp.solutions`). See `INSTALLATION.md` for details.

## Run

```
python test_system.py      (optional: checks your setup)
python virtual_mouse.py
```

Press **Q** in the video window to quit.

## Gestures

| Gesture | Action |
|---------|--------|
| Point with index finger and move | Move cursor |
| Touch thumb + index finger | Left click |
| Touch index + middle finger | Right click |
| Move hand quickly up / down | Scroll up / down |

Keep your index fingertip inside the blue box. Outside the box the cursor does not move.

## Project Files

```
virtual_mouse.py            Main program
config.py                   All settings
requirements.txt            Library versions
README.md                   This file
INSTALLATION.md             Step-by-step setup (Windows / VS Code)
TECHNICAL_DOCUMENTATION.md  How the code works
```

## Settings (config.py)

| Setting | Default | Effect |
|---------|---------|--------|
| `CAMERA_INDEX` | 0 | Which webcam to use |
| `SMOOTH_FACTOR` | 5 | Higher = smoother but slower cursor |
| `CLICK_THRESHOLD` | 40 | Higher = easier to click |
| `SCROLL_THRESHOLD` | 50 | Higher = need faster hand movement to scroll |
| `FRAME_REDUCTION` | 100 | Size of the border outside the active box |
| `CLICK_COOLDOWN_SECONDS` | 0.35 | Minimum time between clicks |
| `SCROLL_SPEED` | 1.0 | Higher = faster scrolling |
| `MIN_DETECTION_CONFIDENCE` / `MIN_TRACKING_CONFIDENCE` | 0.7 | Hand detection strictness |
| `SHOW_FPS`, `SHOW_LANDMARKS`, `SHOW_BOUNDARY`, `SHOW_GESTURE_TEXT` | True | Turn display items on/off |

Save the file and restart the program after changing a setting. If `config.py` is missing, the program uses these defaults.

## Safety and Privacy

- All processing happens on your computer. Nothing is recorded or sent anywhere.
- The cursor stays still while you pinch, so clicks land where you aim.
- `FAILSAFE_ENABLED = True` in `config.py` lets you stop the mouse by moving it to a screen corner.

## Limitations

- Needs good lighting and a fairly plain background
- Tracks one hand by default
- Not meant for gaming or precise professional work

## Credits

MediaPipe (Google) for hand tracking, OpenCV for video, PyAutoGUI for mouse control.
