# Technical Documentation - Virtual Mouse

## 1. Architecture

```
Webcam -> OpenCV (frame) -> MediaPipe Hands (21 landmarks) -> Gesture logic -> PyAutoGUI (mouse)
                                   |                                |
                                   +--> MediaPipe Drawing -----> OpenCV window (video + labels)
```

| Layer | Tools | Role |
|-------|-------|------|
| Front-end (visual output) | OpenCV, MediaPipe Drawing | Live video, red hand skeleton, boundary box, labels, FPS |
| Back-end (logic) | Python, MediaPipe Hands, NumPy, PyAutoGUI | Hand tracking, smoothing, mapping, mouse actions |

## 2. Program flow (`virtual_mouse.py`)

```
start
 |- load settings (config.py, or built-in defaults if missing)
 |- create MediaPipe Hands + drawing tools
 |- open_camera()
 '- loop:
     1. read frame, flip horizontally (mirror)
     2. convert BGR -> RGB, run hands.process()
     3. draw boundary box
     4. if hand found:
          draw skeleton
          get pixel positions of landmarks 0, 4, 8, 12
          if index tip outside box -> show "Move hand inside box"
          else: smooth -> move cursor -> left click -> right click -> scroll
     5. draw FPS, show window
     6. quit when Q is pressed
```

### Functions

| Function | Purpose |
|----------|---------|
| `label()` | Draws a gesture label (respects `SHOW_GESTURE_TEXT`) |
| `open_camera()` | Tries DirectShow then default backend, reads warm-up frames |
| `main()` | Camera loop and all gesture logic |

## 3. Hand landmarks

MediaPipe returns 21 points per hand, each with normalised `x`, `y` (0 to 1).

| Index | Point | Used for |
|-------|-------|----------|
| 0 | Wrist | Scroll |
| 4 | Thumb tip | Left click |
| 8 | Index tip | Cursor and both clicks |
| 12 | Middle tip | Right click |

Pixel position: `pixel_x = int(landmark.x * frame_width)`, `pixel_y = int(landmark.y * frame_height)`.

## 4. Gesture logic

### 4.1 Smoothing
Exponential smoothing reduces jitter:
```python
smooth_x += (index_x - smooth_x) / SMOOTH_FACTOR
smooth_y += (index_y - smooth_y) / SMOOTH_FACTOR
```
Higher `SMOOTH_FACTOR` = smoother but slower response.

### 4.2 Camera to screen mapping
Only the box inside the frame border (`FRAME_REDUCTION`) is used:
```python
screen_x = np.interp(smooth_x, (box, width - box), (0, screen_width))
screen_y = np.interp(smooth_y, (box, height - box), (0, screen_height))
```
Example: 640 px wide frame, box 100: camera range 100 to 540 maps to 0 to 1920.

### 4.3 Left click
`math.dist(thumb, index) < CLICK_THRESHOLD` (pixels).
- One click per pinch (`left_down` flag, reset when fingers separate)
- At least `CLICK_COOLDOWN_SECONDS` between clicks
- The cursor does not move while pinching, so the click lands where aimed

### 4.4 Right click
`math.dist(index, middle) < CLICK_THRESHOLD`, only when not pinching. Same one-click-per-gesture flag and cooldown.

### 4.5 Scroll
```python
move = previous_wrist_y - wrist_y          # positive = hand moved up
if abs(move) > SCROLL_THRESHOLD:
    pyautogui.scroll(int(move / 10 * SCROLL_SPEED))
```
Moving the hand up scrolls up; down scrolls down. The threshold is per frame, so only a quick movement scrolls.

### 4.6 Click state machine
```
fingers apart  --(distance < threshold and cooldown passed)-->  CLICK, mark "down"
mark "down"    --(fingers still together)-->                    no repeat click
mark "down"    --(fingers apart)-->                             reset
```

## 5. Camera handling
`open_camera()` tries `CAP_DSHOW`, then `CAP_ANY` using `CAMERA_INDEX`. Each attempt sets the resolution and reads up to `CAMERA_WARMUP_FRAMES` frames, because some webcams need a few frames before streaming. Returns `None` if nothing works.

## 6. Configuration reference

| Parameter | Default | Effect |
|-----------|---------|--------|
| CAMERA_WIDTH / HEIGHT | 640 / 480 | Capture resolution |
| CAMERA_INDEX | 0 | Webcam number |
| CAMERA_WARMUP_FRAMES | 8 | Frames read before giving up |
| SMOOTH_FACTOR | 5 | Smoothing strength |
| CLICK_COOLDOWN_SECONDS | 0.35 | Minimum gap between clicks |
| CLICK_THRESHOLD | 40 | Pinch distance for clicks (px) |
| SCROLL_THRESHOLD | 50 | Wrist movement needed to scroll (px) |
| FRAME_REDUCTION | 100 | Border excluded from active area (px) |
| MAX_HANDS | 1 | Hands tracked |
| MIN_DETECTION_CONFIDENCE | 0.7 | Detection strictness |
| MIN_TRACKING_CONFIDENCE | 0.7 | Tracking strictness |
| FAILSAFE_ENABLED | False | PyAutoGUI corner failsafe |
| SHOW_FPS / LANDMARKS / BOUNDARY / GESTURE_TEXT | True | Display toggles |
| SCROLL_SPEED | 1.0 | Scroll multiplier |
| MOUSE_MOVE_DURATION | 0 | Cursor move time (0 = instant) |
| LANDMARK_THICKNESS / RADIUS | 2 / 2 | Skeleton drawing size |

## 7. Implementation notes

- `pyautogui.PAUSE = 0` removes PyAutoGUI's default 0.1 s delay per call, which would cap FPS near 10.
- `MPLBACKEND=Agg` stops MediaPipe's matplotlib import from printing the "tkagg interactive backend" message.
- `mp.solutions` exists only in MediaPipe up to about 0.10.14, which is why `requirements.txt` pins that version (with NumPy 1.26.4).
- All processing is local; no frames are saved or sent anywhere.

## 8. Performance (typical mid-range PC)

- FPS: 30 to 60
- Latency: about 50 to 100 ms
- CPU: 15 to 30 %

Tips: good lighting, plain background, lower resolution if FPS is low.

## 9. Testing

- `python test_system.py` checks Python, OpenCV, MediaPipe (`solutions` present), PyAutoGUI, NumPy and webcam frames.
- `python inspect_mediapipe.py` prints the MediaPipe version and whether `solutions` exists.

## 10. Possible improvements

Double click, drag and drop, two-hand gestures, calibration mode, multi-monitor support, saved gesture profiles.

---
Document version 2.0
