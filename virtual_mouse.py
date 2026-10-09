"""
Virtual Mouse using Hand Gestures
=================================
Move cursor : point with your index finger
Left click  : touch thumb + index finger (pinch)
Right click : touch index + middle finger
Scroll      : move your hand quickly up / down
Quit        : press Q

All settings are in config.py
"""

import os
os.environ["MPLBACKEND"] = "Agg"           # hides the "tkagg interactive mode" message
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"   # hides MediaPipe log noise

import math
import time

import cv2
import mediapipe as mp
import numpy as np
import pyautogui

import config as cfg

pyautogui.FAILSAFE = cfg.FAILSAFE_ENABLED
pyautogui.PAUSE = 0                         # no delay after each mouse action
SCREEN_W, SCREEN_H = pyautogui.size()
RED, GREEN, BLUE = (0, 0, 255), (0, 255, 0), (255, 0, 0)
FONT = cv2.FONT_HERSHEY_SIMPLEX

# MediaPipe hand tracking + drawing
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands(
    max_num_hands=cfg.MAX_HANDS,
    min_detection_confidence=cfg.MIN_DETECTION_CONFIDENCE,
    min_tracking_confidence=cfg.MIN_TRACKING_CONFIDENCE,
)
dot_style = mp_draw.DrawingSpec(color=RED, thickness=cfg.LANDMARK_THICKNESS,
                                circle_radius=cfg.LANDMARK_RADIUS)


def open_camera():
    """Open the webcam (tries DirectShow first, then the default backend)."""
    for backend in (cv2.CAP_DSHOW, cv2.CAP_ANY):
        cap = cv2.VideoCapture(cfg.CAMERA_INDEX, backend)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, cfg.CAMERA_WIDTH)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, cfg.CAMERA_HEIGHT)
        for _ in range(cfg.CAMERA_WARMUP_FRAMES):   # some webcams need a few frames
            if cap.read()[0]:
                return cap
            time.sleep(0.03)
        cap.release()
    return None


def main():
    cap = open_camera()
    if cap is None:
        print("Could not open webcam. Close Zoom/Teams or change CAMERA_INDEX in config.py")
        return

    box = cfg.FRAME_REDUCTION          # active area = camera frame minus this border
    smooth_x = smooth_y = None         # smoothed finger position
    left_down = right_down = False     # makes one pinch = one click
    last_click = 0                     # time of the last click
    prev_wrist_y = None                # used for scrolling
    prev_time = time.time()

    print("Virtual Mouse started. Press Q in the video window to quit.")

    while True:
        ok, frame = cap.read()
        if not ok:
            print("Could not read from webcam.")
            break
        frame = cv2.flip(frame, 1)                        # mirror the image
        h, w = frame.shape[:2]
        results = hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

        if cfg.SHOW_BOUNDARY:
            cv2.rectangle(frame, (box, box), (w - box, h - box), BLUE, 2)

        if results.multi_hand_landmarks:
            hand = results.multi_hand_landmarks[0]
            if cfg.SHOW_LANDMARKS:
                mp_draw.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS,
                                       dot_style, dot_style)

            # Pixel position of a landmark: 0=wrist, 4=thumb tip, 8=index tip, 12=middle tip
            def point(i):
                return int(hand.landmark[i].x * w), int(hand.landmark[i].y * h)
            wrist, thumb, index, middle = point(0), point(4), point(8), point(12)

            if not (box <= index[0] <= w - box and box <= index[1] <= h - box):
                cv2.putText(frame, "Move hand inside box", (50, 100), FONT, 0.8, (0, 255, 255), 2)
                prev_wrist_y = wrist[1]
            else:
                # 1) Smooth the index finger position (less jitter)
                if smooth_x is None:
                    smooth_x, smooth_y = index
                smooth_x += (index[0] - smooth_x) / cfg.SMOOTH_FACTOR
                smooth_y += (index[1] - smooth_y) / cfg.SMOOTH_FACTOR

                pinch = math.dist(thumb, index) < cfg.CLICK_THRESHOLD
                now = time.time()
                can_click = now - last_click > cfg.CLICK_COOLDOWN_SECONDS

                # 2) Move the cursor (camera box -> full screen); stay still while pinching
                if not pinch:
                    screen_x = np.interp(smooth_x, (box, w - box), (0, SCREEN_W))
                    screen_y = np.interp(smooth_y, (box, h - box), (0, SCREEN_H))
                    pyautogui.moveTo(int(screen_x), int(screen_y))

                # 3) Left click: thumb + index close together
                if pinch:
                    if not left_down and can_click:
                        pyautogui.click()
                        left_down, last_click = True, now
                    cv2.putText(frame, "LEFT CLICK", (50, 100), FONT, 1, GREEN, 2)
                else:
                    left_down = False

                # 4) Right click: index + middle close together
                if math.dist(index, middle) < cfg.CLICK_THRESHOLD and not pinch:
                    if not right_down and can_click:
                        pyautogui.rightClick()
                        right_down, last_click = True, now
                    cv2.putText(frame, "RIGHT CLICK", (50, 150), FONT, 1, RED, 2)
                else:
                    right_down = False

                # 5) Scroll: wrist moves up/down quickly
                if prev_wrist_y is not None:
                    move = prev_wrist_y - wrist[1]        # positive = hand moved up
                    if abs(move) > cfg.SCROLL_THRESHOLD:
                        pyautogui.scroll(int(move / 10 * cfg.SCROLL_SPEED))
                        cv2.putText(frame, "SCROLL", (50, 200), FONT, 1, (255, 255, 0), 2)
                prev_wrist_y = wrist[1]

            cv2.putText(frame, "Hand Detected", (10, 60), FONT, 0.7, GREEN, 2)
        else:
            cv2.putText(frame, "No Hand Detected", (10, 60), FONT, 0.7, RED, 2)

        if cfg.SHOW_FPS:
            now = time.time()
            cv2.putText(frame, f"FPS: {int(1 / max(now - prev_time, 0.001))}", (10, 30),
                        FONT, 0.7, (255, 0, 255), 2)
            prev_time = now

        cv2.imshow("Virtual Mouse", frame)
        if cv2.waitKey(1) & 0xFF in (ord("q"), ord("Q")):
            break

    cap.release()
    cv2.destroyAllWindows()
    print("Virtual Mouse stopped.")


if __name__ == "__main__":
    main()





# run this to install all modules: "C:/Users/varun/AppData/Local/Programs/Python/Python312/python.exe" -m pip install -r requirements.txt