import pyautogui
import sys, os, time
import pandas

def saveScript(actions, scriptName):
    """
    Saves the commands from the list widget from the automation app to a .txt file in the relative directory /data
    :param actions: list 
    :param scriptName: str
    :return: None
    """
    file_path = os.path.join('scripts', scriptName)
    # Check if directory exists, if not, create the directory
    if not os.path.isdir('scripts'):
        os.mkdir('scripts')
    first = True
    with open(f'{file_path}.txt', 'w') as output:
        for action in actions:
            # The first action will not create a new line
            if first:
                first = False
                output.write(action)
            else:
                output.write(f'\n{action}')
    output.close()
    return True

def runScript(scriptName, dataFile):
    """
    Reads the given .txt file and runs the commands in order using pyautogui
    :param scriptName: str
    :return: None
    """
    file_path = os.path.join('scripts', scriptName)
    script = open(file_path, 'r')
    actions = script.read().split('\n')
    delay = 0 
    if actions[0]:
        for action in actions:
            if action[0:2] == 'De':
                delay = handleDelay(action)

            elif action[0] == 'L':
                handleClick(action, delay)
                delay = 0

            elif action[0] == 'K' or action[0] == 'T':
                time.sleep(delay)
                delay = 0
                handleKeyboardInput(action)

            elif action[0:2] == 'Da':
                time.sleep(delay)
                delay = 0
                handleDataEntry(action, dataFile)

        

def handleClick(action, delay=0):
    """
    Handles reading the given command and registering a left click at the desired coordinates
    :param action: str
    :return: None
    """
    x = ''
    y = ''
    i = 13
    while action[i] != ',':
        x += action[i]
        i = i + 1
    i = i + 2
    while action[i] != ')':
        y += action[i]
        i = i + 1
    pyautogui.click(int(x), int(y), duration=delay)


def handleDataEntry(action, dataFile):
    """
    Handles reading the given command and outputting a value (str) from a Label/Value pair in chosen .csv file
    :param action: str
    :return: None
    """
    label = action[17:]
    dataDict = pandas.read_csv(dataFile,names=['Label', 'Value'], index_col=0).to_dict('index')
    pyautogui.write(dataDict[label]['Value'])


def handleKeyboardInput(action):
    """
    Handles reading the given command and registering a keystroke or outputting given text input
    :param action: str
    :return: None
    """

    if action[0] == 'K':
        entry = action[11:]
        pyautogui.press(entry)
    else:
        entry = action[22:]
        pyautogui.write(entry)


def handleDelay(action):
    """
    Handles reading the given command and registering a time delay in seconds
    :param action: str
    :return: float
    """
    i = 7
    delay = ''
    while action[i] != 's':
        delay += action[i]
        i = i + 1
    return float(delay)

def deleteScript(scriptName):
    """
    Deletes the script that is highlighted in the treeView widget in the Automation app
    :param scriptName: str
    :return: None
    """
    dirpath = os.path.join(os.getcwd(), 'scripts')
    for path, directories, files in os.walk(dirpath):
        for file in files:
            if file == scriptName:
                os.remove(os.path.join(dirpath, file))