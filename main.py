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
from utils import get_game_window, bring_game_to_foreground, take_screenshot, check_for_templates, find_and_right_click, find_and_lef_click

GAME_WINDOW_TITLE = "Path of Exile"

pyautogui.FAILSAFE = False  # Disable PyAutoGUI fail-safes

# Load images for template matching
template_alt = cv2.imread('img/alteration.png', cv2.IMREAD_GRAYSCALE)
template_aug = cv2.imread('img/alg.png', cv2.IMREAD_GRAYSCALE)
template_match = cv2.imread('img/match.png', cv2.IMREAD_GRAYSCALE)
template_item = cv2.imread('img/match.png', cv2.IMREAD_GRAYSCALE)

game_window = get_game_window(GAME_WINDOW_TITLE)

bring_game_to_foreground(game_window)
time.sleep(1)

while True:
    screenshot = take_screenshot(get_game_window(GAME_WINDOW_TITLE))

    if check_for_templates(screenshot, template_match):
        break
    else:
        check_for_templates(screenshot, template_match)
        if find_and_right_click(screenshot, template_alt):
            print("Alteration found and right-clicked.")
        time.sleep(0.5)
        if find_and_lef_click(screenshot, template_item):
            print("bateu alt")
        break
