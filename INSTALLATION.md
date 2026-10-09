# Installation Guide (Windows + VS Code)

## 1. Install Python 3.12

Download Python 3.12 from python.org. During setup, tick **Add Python to PATH**.

## 2. Put all project files in one folder

At minimum: `virtual_mouse.py`, `config.py`, `requirements.txt`. (Without `config.py` the program still runs using default settings.)

## 3. Install the libraries

Open a terminal **inside the project folder**.

Command Prompt:
```
python -m pip install -r requirements.txt
```

PowerShell with a full Python path (note the `&`):
```
& "C:/Users/varun/AppData/Local/Programs/Python/Python312/python.exe" -m pip install -r requirements.txt
```

Warnings such as "scripts are not on PATH" are harmless.

### Why the versions are pinned

| Package | Version | Reason |
|---------|---------|--------|
| mediapipe | 0.10.14 | Newer releases removed `mp.solutions`, which this project uses |
| numpy | 1.26.4 | MediaPipe 0.10.14 needs NumPy 1.x |
| opencv-python | 4.10.0.84 | Works with NumPy 1.26 |
| pyautogui | 0.9.53 or newer | Mouse control |

## 4. Verify

```
python -c "import mediapipe as mp; print(mp.__version__, hasattr(mp,'solutions'))"
```
Expected output: `0.10.14 True`

Then run `python test_system.py`. All six checks should pass.

## 5. VS Code: select the right Python

1. Press `Ctrl+Shift+P`
2. Choose **Python: Select Interpreter**
3. Pick **Python 3.12** (`...\Python312\python.exe`)
4. If warnings stay, run **Developer: Reload Window**

This fixes "No module named mediapipe" and the `reportMissingImports` warning.

## 6. Run

```
python virtual_mouse.py
```
