from automationApp import AutomationApp
from PySide6.QtWidgets import QApplication

def run():
    app = QApplication([])
    ex  = AutomationApp()
    app.exec()

if __name__ == '__main__':
    run()