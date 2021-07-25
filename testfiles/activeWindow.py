import pyautogui

fw = pyautogui.getAllWindows()
for window in fw:
    print(window.title)
    print(window.size)