import pyautogui
import pandas
import time
fw = pyautogui.getWindowsWithTitle('New Tab - Google Chrome')[0]

dataDict = pandas.read_csv('exampleData.csv',names=['Title', 'Value'], index_col=0).to_dict('index')

fw.width = 1920/2
fw.height = 1800
fw.topleft = (0, 0)

#click and type URL
pyautogui.click(163,64,duration=.10) 
pyautogui.write('gmail.com')
pyautogui.write(['enter'])
pyautogui.click(341, 752,duration=1.25) # click create account
pyautogui.click(353,808,duration=0.2) # for myself
time.sleep(.75)
pyautogui.write(dataDict['First']['Value']) # type First Name
pyautogui.click(349, 505) # Click Last Name
pyautogui.write(dataDict['Last']['Value'])
pyautogui.click(186,570) # Click username
pyautogui.write(dataDict['Email']['Value'])
time.sleep(0.25)
pyautogui.click(186,649) # Click password
pyautogui.write(dataDict['Password']['Value'])
pyautogui.click(375,646) # Click confirm
pyautogui.write(dataDict['Password']['Value'])

pyautogui.click(463,821) # Click next
time.sleep(1.25)
pyautogui.write(dataDict['Phone']['Value'])

# pyautogui.click()
# pyautogui.click()

