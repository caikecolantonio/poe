import tkinter as tk
import threading
import time
import pyautogui
import cv2
from utils import get_game_window, bring_game_to_foreground, take_screenshot, check_for_templates, find_and_right_click, click_in_fixed_region, move_mouse_away

# Game-related variables and setup
GAME_WINDOW_TITLE = "Path of Exile"
pyautogui.FAILSAFE = False  # Disable PyAutoGUI fail-safes
template_alt = cv2.imread('img/alteration.png', cv2.IMREAD_GRAYSCALE)
template_aug = cv2.imread('img/alg.png', cv2.IMREAD_GRAYSCALE)
template_match = cv2.imread('img/match.png', cv2.IMREAD_GRAYSCALE)
template_item = cv2.imread('img/match.png', cv2.IMREAD_GRAYSCALE)
item_format_region = (300, 370, 100, 100)
game_window = get_game_window(GAME_WINDOW_TITLE)

# GUI setup
root = tk.Tk()
root.title("Game Automation")
root.geometry("300x200")

run_count = 0
template_check_count = 0
is_running = False
game_thread = None

# Function to handle play button click
def play():
    global run_count, is_running, game_thread
    if not is_running:
        is_running = True
        run_count += 1
        count_label.config(text=f"Runs: {run_count}")
        bring_game_to_foreground(game_window)
        # Start the game loop in a new thread
        game_thread = threading.Thread(target=run_game_loop)
        game_thread.start()

# Function to stop the game loop
def stop():
    global is_running
    if is_running:
        is_running = False
        print("Stopping the script.")
        if game_thread is not None:
            game_thread.join()  # Wait for the game loop to finish
    root.quit()

# Game loop function
def run_game_loop():
    global template_check_count, is_running

    while is_running:
        screenshot = take_screenshot(get_game_window(GAME_WINDOW_TITLE))
        
        # Increment the template check counter
        template_check_count += 1
        template_check_label.config(text=f"Template Checks: {template_check_count}")
        
        if check_for_templates(screenshot, template_match):
            print("Template match found, breaking the loop.")
            break  # Exit loop if match is found
        else:
            if find_and_right_click(screenshot, template_alt):
                print("Alteration found and right-clicked.")
            time.sleep(0.5)
            
            if click_in_fixed_region(game_window, item_format_region):
                print("Clicked in fixed region (Alt)")
            time.sleep(0.5)
            
            if find_and_right_click(screenshot, template_aug):
                print("Augmentation found and right-clicked.")
            time.sleep(0.5)
            
            if click_in_fixed_region(game_window, item_format_region):
                print("Clicked in fixed region (Aug)")
            time.sleep(0.5)
            
            move_mouse_away()
            time.sleep(0.5)

# Function to handle ESC key press
def on_esc_press(event):
    print("ESC pressed. Stopping the script.")
    stop()

# Create a label to display the count
count_label = tk.Label(root, text=f"Runs: {run_count}", font=("Arial", 16))
count_label.pack(pady=20)

# Create a label to display the template check count
template_check_label = tk.Label(root, text=f"Template Checks: {template_check_count}", font=("Arial", 16))
template_check_label.pack(pady=10)

# Create a play button
play_button = tk.Button(root, text="Play", font=("Arial", 14), command=play)
play_button.pack(pady=10)

# Create a stop button
stop_button = tk.Button(root, text="Stop", font=("Arial", 14), command=stop)
stop_button.pack(pady=10)

# Bind the "ESC" key to the root window
root.bind('<Escape>', on_esc_press)

# Start the tkinter main loop
root.mainloop()

# Join the game thread after the main loop is finished
if game_thread is not None:
    game_thread.join()
