import pyautogui
import time

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 1

print("Screen size:", pyautogui.size())
pyautogui.moveTo(100, 100, duration=1)
print("Mouse at:", pyautogui.position())

"""pyautogui.FAILSAFE = True
pyautogui.PAUSE = 10.0
print("Screen size:", pyautogui.size())
print("Mouse at:", pyautogui.position())"""