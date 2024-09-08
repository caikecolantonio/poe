import pygetwindow as gw
import cv2
import time
import numpy as np
import mss
import pyautogui


def get_game_window(title):
    try:
        window = gw.getWindowsWithTitle(title)[0]
        return window
    except IndexError:
        print("Game window not found.")
        exit(1)

def bring_game_to_foreground(game_window):
    game_window.restore()
    game_window.activate()
    time.sleep(1)

def take_screenshot(game_window):
    with mss.mss() as sct:
        region = {"left": game_window.left, "top": game_window.top, "width": game_window.width, "height": game_window.height}
        screenshot = np.array(sct.grab(region))
        screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGRA2RGB)
        return screenshot
    
def check_for_templates(screenshot, template):
    gray_screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2GRAY)
    res = cv2.matchTemplate(gray_screenshot, template, cv2.TM_CCOEFF_NORMED)
    threshold = 0.9
    loc = np.where(res >= threshold)
    return len(loc[0]) > 0

def find_and_right_click(screenshot, alteration_template):
    gray_screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2GRAY)
    res = cv2.matchTemplate(gray_screenshot, alteration_template, cv2.TM_CCOEFF_NORMED)
    threshold = 0.8
    loc = np.where(res >= threshold)
    
    if len(loc[0]) > 0:
        # Get the position of the first match
        top_left = (loc[1][0], loc[0][0])  # x, y of the first matched point
        # Find the center of the alteration for a precise click
        h, w = alteration_template.shape[:2]
        center_x = top_left[0] + w // 2
        center_y = top_left[1] + h // 2
        
        # Simulate a right-click at the center of the alteration
        pyautogui.rightClick(center_x, center_y)
        print(f"Right-clicked at position: ({center_x}, {center_y})")
        return True
    return False

def find_and_lef_click(screenshot, alteration_template):
    gray_screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2GRAY)
    res = cv2.matchTemplate(gray_screenshot, alteration_template, cv2.TM_CCOEFF_NORMED)
    threshold = 0.8
    loc = np.where(res >= threshold)
    
    if len(loc[0]) > 0:
        # Get the position of the first match
        top_left = (loc[1][0], loc[0][0])  # x, y of the first matched point
        # Find the center of the alteration for a precise click
        h, w = alteration_template.shape[:2]
        center_x = top_left[0] + w // 2
        center_y = top_left[1] + h // 2
        
        # Simulate a right-click at the center of the alteration
        pyautogui.leftClick(center_x, center_y)
        print(f"Left-clicked at position: ({center_x}, {center_y})")
        return True
    return False