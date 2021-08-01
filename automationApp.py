from scriptHandling import deleteScript, runScript, saveScript
import pyautogui, os
from PySide6.QtWidgets import (QDialog, QFileDialog, QFrame, QLabel, QWidget, QPushButton, QGridLayout,
 QMessageBox, QListWidget, QInputDialog, QTabWidget, QVBoxLayout, QFileSystemModel, QTreeView)
from PySide6.QtGui import QCloseEvent, QIcon
import ctypes

class AutomationApp(QDialog):
    """
    Main container class for the automation
    """
    def __init__(self):
        super().__init__()
        self.setup()

    def setup(self):
        self.setGeometry(400, 300, 500, 500)
        self.setWindowTitle('Mouse & Keyboard Automation Tool')
        vbox = QVBoxLayout()
        tabWidget = QTabWidget()
        tabWidget.addTab(TabCreate(), "Create Script")
        tabWidget.addTab(TabRun(), "Run Script")
        vbox.addWidget(tabWidget)
        self.setLayout(vbox)
        self.setIcon()
        self.show()


    def setIcon(self):
        appIcon = QIcon("keyboardIcon.jpg")
        myappid = u'keyboardIcon.jpg'
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        self.setWindowIcon(appIcon)
        
    # def closeEvent(self, event: QCloseEvent):
    #     reply = QMessageBox.question(self, 'Message', 'Are you sure you want to quit?',
    #                                 QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

    #     if reply == QMessageBox.Yes:
    #         event.accept()
    #     else:
    #         event.ignore()

class TabCreate(QWidget):
    """
    Container class for the widgets found in the create script tab.
    """
    def __init__(self):
        super().__init__()
        self.setup()
        
    def setup(self):
        """
        Build and organize the widgets within the "Create Script" tab.
        """
        self.listWidget()
        self.mouseClickButton()
        self.dataEntryButton()
        self.typedTextButton()
        self.deleteInputButton()
        self.delayButton()
        self.saveScriptButton()
        windowLayout = QGridLayout()
        vBox = QVBoxLayout()
        windowLayout.setColumnMinimumWidth(1,280)
        windowLayout.setColumnMinimumWidth(0, 130)
        vBox.addWidget(self.btn_mouse)
        vBox.addWidget(self.btn_text)
        vBox.addWidget(self.btn_keyboard)
        vBox.addWidget(self.btn_delay)
        vBox.addWidget(self.btn_delete)
        vBox.addWidget(self.btn_save)
        windowLayout.addLayout(vBox, 0, 0)
        windowLayout.addWidget(self.listW, 0, 1)
        self.setLayout(windowLayout)     

    def dataEntryButton(self):
        self.btn_text = QPushButton('Data Entry/Keystrokes', self)
        self.btn_text.clicked.connect(self.launch_dataEntryPopup)
        self.btn_text.setFixedSize(130, 30)
        self.btn_text.move(50, 50)

    def typedTextButton(self):
        self.btn_keyboard = QPushButton('Typed Keyboard Text', self)
        self.btn_keyboard.clicked.connect(self.launch_typedTextPopup)
        self.btn_keyboard.setFixedSize(130, 30)
        self.btn_keyboard.move(50, 50)

    def mouseClickButton(self):
        self.btn_mouse = QPushButton('Mouse Left Click', self)
        self.btn_mouse.clicked.connect(self.launch_mouseClickPopup)
        self.btn_mouse.setFixedSize(130, 30)
        self.btn_mouse.move(50, 20)

    def delayButton(self):
        self.btn_delay = QPushButton('Delay', self)
        self.btn_delay.clicked.connect(self.launch_delaypopup)
        self.btn_delay.setFixedSize(130, 30)
        self.btn_delay.move(50, 20)

    def deleteInputButton(self):
        self.btn_delete = QPushButton('Delete Input', self)
        self.btn_delete.clicked.connect(self.deleteListEntry)
        self.btn_delete.setFixedSize(130, 30)
        self.btn_delete.move(50, 140)
    
    def saveScriptButton(self):
        self.btn_save = QPushButton('Save Script', self)
        self.btn_save.clicked.connect(self.launch_saveScriptPopup)
        self.btn_save.setFixedSize(130, 30)
        self.btn_save.move(50, 50)

    def listWidget(self):
        self.listW = QListWidget(self)
        self.listW.setAlternatingRowColors(True)
        self.listW.resize(280, 390)
        self.listW.move(180, 20)

    def addToListDataEntry(self, entry):
        if entry[0:9] == 'Keystroke':
            self.listW.addItem(entry)
        else:
            self.listW.addItem(f'Data File Input: {entry}')

    def addToListTypedText(self, entry):
        self.listW.addItem(f'Typed Keyboard Input: {entry}')

    def addToListMouseClick(self):
        position = pyautogui.position()
        self.listW.addItem(f'Left Click: ({position[0]}, {position[1]})')

    def addToListDelay(self, entry):
        self.listW.addItem(f'Delay: {entry}s')

    def deleteListEntry(self):
        item = self.listW.row(self.listW.currentItem())
        self.listW.takeItem(item)

    def launch_dataEntryPopup(self):
        """
        Popup window that launches when the 'Data Entry/Keystrokes' button is pressed. The user may select from the the dropdown list of
        what data or keystrokes they want to recorded.
        """
        items = ['First Name', 'Last Name', 'Email', 'Phone', 'Branch', 'Title', 'Password', 'Keystroke: enter', 'Keystroke: tab']
        item, ok = QInputDialog.getItem(self, 'Data Entry & Keystroke Inputs', 'Choose a data entry or keystroke', items, 0, False)
        if ok and item:
            self.addToListDataEntry(item)

    def launch_typedTextPopup(self):
        """
        Popup window that launches when the 'typedTextPopup' button is pressed. The user may type any text they want directly reproduced by the 
        script.
        """
        text, ok = QInputDialog.getText(self, 'Typed Text Input', 'Type any text here (e.g. website name)')
        if ok and text:
            self.addToListTypedText(text)

    def launch_mouseClickPopup(self):
        """
        Popup window that launches when the 'Mouse Left Click' button is pressed. By pressing the 'Record', the current mouse coordinates
        will be saved onto the current list widget.
        """
        dialog = QDialog(self)
        label = QLabel(self)
        label.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        label.setText('Hover mouse over desired location and press ENTER to record a click. \n Press ESC or "X" out this window to cancel.')
        dialog.setWindowTitle('Mouse Click')
        btn_record = QPushButton('Record')
        btn_record.setDefault(True)
        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(btn_record)
        dialog.setLayout(layout)
        btn_record.clicked.connect(dialog.accept)
        if dialog.exec() == QDialog.Accepted:
            self.addToListMouseClick()

    def launch_saveScriptPopup(self):
        """
        Popup window that launches when the 'Save Script' button is pressed. This will save the current list of commands in the list widget onto a .txt
        with the name filled into the input dialog.
        """
        scripts_dirpath = os.path.join(os.getcwd(), 'scripts')
        items = [self.listW.item(x).text() for x in range(self.listW.count())]
        text, ok = QInputDialog.getText(self, 'Save Script', 'Script Name:')
        if ok and text:
            for path, directories, files in os.walk(scripts_dirpath):
                for file in files:
                    if text + '.txt' == file:
                        override = self.launch_duplicateWarning(items, text)
                        break
                else:
                    saveScript(items, text)

    def launch_duplicateWarning(self, items, scriptName):
        """
        Popup window that launches when the when another file shares the name currently trying to be saved from the saveScriptPopup. Warns user about duplicate
        and asks if the user would like to overwrite the file.
        param items: list scriptName: str
        """
        warningDialog = QMessageBox()
        warningDialog.setWindowTitle('Overwrite Warning')
        warningDialog.setText(f'A file with the name {scriptName}.txt already exists, do you want to replace it?')
        warningDialog.setIcon(QMessageBox.Warning)
        warningDialog.setStandardButtons(QMessageBox.Cancel|QMessageBox.Ok)
        warningDialog.setDefaultButton(QMessageBox.Cancel)
        response = warningDialog.exec()
        if response == QMessageBox.Ok:
            saveScript(items, scriptName)

    def launch_delaypopup(self):
        d, ok = QInputDialog.getDouble(self, 'Delay', 'Delay Amount (seconds):', 1, 0.25, 100, 2, step=0.25)
        if ok and d:
            self.addToListDelay(d)
    

class TabRun(QWidget):
    """
    Container class for widgets found in run script tab.
    """
    def __init__(self):
        super().__init__()
        self.setup()
        
    def setup(self):
        """
        Build and organize the widgets within the "Run Script" tab.
        """
        self.dirpath = os.path.join(os.getcwd(), 'scripts')
        self.treeWidget()
        self.runScriptButton()
        self.deleteScriptButton()
        windowLayout = QVBoxLayout()
        windowLayout.addWidget(self.tree)
        windowLayout.addWidget(self.btn_run)
        windowLayout.addWidget(self.btn_delete)
        self.setLayout(windowLayout)        

    def runScriptButton(self):
        self.btn_run = QPushButton('Run', self)
        self.btn_run.clicked.connect(self.launch_runPopup)
        self.btn_run.setFixedHeight(35)
        self.btn_run.move(50, 20)

    def deleteScriptButton(self):
        self.btn_delete = QPushButton('Delete', self)
        self.btn_delete.clicked.connect(self.launch_deletePopup)
        self.btn_delete.setFixedHeight(35)
        self.btn_delete.move(50, 100)

    def treeWidget(self):
        self.model = QFileSystemModel()
        self.model.setRootPath(self.dirpath)
        self.tree = QTreeView()
        self.tree.setModel(self.model)
        self.tree.setRootIndex(self.model.index(self.dirpath))
        self.tree.setAnimated(False)
        self.tree.setIndentation(20)
        self.tree.setSortingEnabled(True)
        self.tree.setColumnWidth(0, 250)
        self.tree.setAlternatingRowColors(True)
        self.tree.setWindowTitle("Dir View")
        self.tree.resize(100, 100)
    
    def launch_deletePopup(self):
        """
        Popup window that launches when the 'delete' button is pressed. Asks user for confirmation of deleting a script file.
        """
        deleteMessage = QMessageBox()
        deleteMessage.setWindowTitle('Deleting Script')
        deleteMessage.setText('Are you sure you want to delete this script?')
        deleteMessage.setIcon(QMessageBox.Question)
        deleteMessage.setStandardButtons(QMessageBox.Cancel|QMessageBox.Ok)
        deleteMessage.setDefaultButton(QMessageBox.Cancel)
        response = deleteMessage.exec()
        if response == QMessageBox.Ok: 
            index = self.tree.currentIndex()
            scriptName = self.model.fileName(index)
            deleteScript(scriptName)

    def launch_runPopup(self):
        """
        Popup window that launches when the 'Run' button is pressed. The currently selected script on the treewidget will run. The popup prompts the user
        to select a data file from which the script will copy its data entries.
        """
        data_dirpath = os.path.join(os.getcwd(), 'data')
        file_filter = 'Data File (*.xlsx *.csv *.dat);; Excel File (*.xlsx *.xls)'
        response = QFileDialog.getOpenFileName(
            parent=self,
            caption='Select a data file',
            dir=data_dirpath,
            filter=file_filter,
            selectedFilter='Data File (*.xlsx *.csv *.dat)'
        )
        if response[0]:        
            index = self.tree.currentIndex()
            scriptName = self.model.fileName(index)
            runScript(scriptName, response[0])
