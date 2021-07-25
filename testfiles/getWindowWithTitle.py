import pyautogui

fw = pyautogui.getWindowsWithTitle('chrome')
fw=fw[0]



fw.width = 1920/2
fw.height = 1800
fw.topleft = (0, 0)