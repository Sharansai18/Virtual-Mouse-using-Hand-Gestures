"""
Configuration File for Virtual Mouse
=====================================

Modify these parameters to customize your virtual mouse behavior.
After changing values, save this file and restart the program.
"""

# ============================================
# CAMERA SETTINGS
# ============================================

# Camera resolution (lower = faster but less accurate)
CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480

# Camera index (0 = default camera, 1 = second camera, etc.)
CAMERA_INDEX = 0

# Number of warmup reads before camera is treated as unavailable
# Helps webcams that need a few frames to start streaming
CAMERA_WARMUP_FRAMES = 8


# ============================================
# SMOOTHING SETTINGS
# ============================================

# Number of previous positions to average for smooth movement
# Higher = smoother but slower response
# Lower = faster but more jittery
# Recommended: 3-7
SMOOTH_FACTOR = 6

# Minimum gap between left clicks in seconds
# Prevents accidental rapid double clicks
CLICK_COOLDOWN_SECONDS = 0.35


# ============================================
# GESTURE SENSITIVITY
# ============================================

# Distance threshold for click detection (in pixels)
# Lower = easier to trigger clicks
# Higher = need closer pinch to click
# Recommended: 30-50
CLICK_THRESHOLD = 41

# Distance threshold for scroll detection (in pixels)
# Lower = more sensitive scrolling
# Higher = need more movement to scroll
# Recommended: 40-60
SCROLL_THRESHOLD = 55


# ============================================
# SCREEN MAPPING
# ============================================

# Frame reduction from edges (in pixels)
# Prevents cursor from going to screen edges unintentionally
# Higher = smaller active area but more stable
# Recommended: 80-120
FRAME_REDUCTION = 100


# ============================================
# HAND DETECTION SETTINGS
# ============================================

# Maximum number of hands to detect
# 1 = better performance, 2 = can use both hands
MAX_HANDS = 1

# Minimum confidence for hand detection (0.0 to 1.0)
# Higher = fewer false detections but may miss hands
# Recommended: 0.5-0.8
MIN_DETECTION_CONFIDENCE = 0.7

# Minimum confidence for hand tracking (0.0 to 1.0)
# Higher = more stable tracking but may lose hand
# Recommended: 0.5-0.8
MIN_TRACKING_CONFIDENCE = 0.7


# ============================================
# SAFETY SETTINGS
# ============================================

# PyAutoGUI failsafe (move mouse to corner to stop)
# True = enabled (safer), False = disabled (more convenient)
FAILSAFE_ENABLED = False


# ============================================
# DISPLAY SETTINGS
# ============================================

# Show FPS on screen
SHOW_FPS = True

# Show hand landmarks
SHOW_LANDMARKS = True

# Show boundary box
SHOW_BOUNDARY = True

# Show gesture indicators
SHOW_GESTURE_TEXT = True


# ============================================
# ADVANCED SETTINGS (modify with caution)
# ============================================

# Scroll speed multiplier
# Higher = faster scrolling
SCROLL_SPEED = 1.0

# Mouse movement duration (0 = instant, higher = slower)
# Recommended: 0 for best performance
MOUSE_MOVE_DURATION = 0

# Landmark drawing thickness
LANDMARK_THICKNESS = 2

# Landmark circle radius
LANDMARK_RADIUS = 2


# ============================================
# PRESETS
# ============================================

# Uncomment one of these preset configurations:

# PRESET 1: PRECISE (better accuracy, slower)
# SMOOTH_FACTOR = 7
# CLICK_THRESHOLD = 35
# FRAME_REDUCTION = 120

# PRESET 2: FAST (faster response, less accurate)
# SMOOTH_FACTOR = 3
# CLICK_THRESHOLD = 45
# FRAME_REDUCTION = 80

# PRESET 3: BALANCED (default)
# SMOOTH_FACTOR = 5
# CLICK_THRESHOLD = 40
# FRAME_REDUCTION = 100
