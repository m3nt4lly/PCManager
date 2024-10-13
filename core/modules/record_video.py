import cv2
import pyautogui
import numpy as np
import time


def record_screen(output_filename, duration=10):
    screen_size = pyautogui.size()
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_filename, fourcc, 15.0, screen_size)

    start_time = time.time()

    while (time.time() - start_time) < duration:
        screenshot = pyautogui.screenshot()
        frame = np.array(screenshot)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        out.write(frame)

    out.release()