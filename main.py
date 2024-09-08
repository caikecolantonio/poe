import tkinter as tk
import pyautogui
import numpy as np
import cv2
import pygetwindow as gw
import time
import keyboard
import mss
import os
from dotenv import load_dotenv
from utils import get_game_window, bring_game_to_foreground, take_screenshot, check_for_templates, find_and_right_click, click_in_fixed_region, move_mouse_away

GAME_WINDOW_TITLE = "Path of Exile"

pyautogui.FAILSAFE = False  # Disable PyAutoGUI fail-safes

# Load images for template matching
template_alt = cv2.imread('img/alteration.png', cv2.IMREAD_GRAYSCALE)
template_aug = cv2.imread('img/alg.png', cv2.IMREAD_GRAYSCALE)
template_match = cv2.imread('img/match.png', cv2.IMREAD_GRAYSCALE)
template_item = cv2.imread('img/match.png', cv2.IMREAD_GRAYSCALE)
item_format_region = (300, 370, 100, 100)
game_window = get_game_window(GAME_WINDOW_TITLE)

bring_game_to_foreground(game_window)
time.sleep(1)

for x in range(20):
    screenshot = take_screenshot(get_game_window(GAME_WINDOW_TITLE))

    if check_for_templates(screenshot, template_match):
        break
    else:
        check_for_templates(screenshot, template_match)
        if find_and_right_click(screenshot, template_alt):
            print("Alteration found and right-clicked.")
        time.sleep(0.5)
        if click_in_fixed_region(game_window, item_format_region):
            print("bateu alt")
        time.sleep(0.5)
        if find_and_right_click(screenshot, template_aug):
            print("Alteration found and right-clicked.")
        time.sleep(0.5)
        if click_in_fixed_region(game_window, item_format_region):
            print("bateu alg")
        time.sleep(0.5)
        move_mouse_away()
        time.sleep(0.5)
