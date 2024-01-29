# importing required libraries
from datetime import datetime
from PyQt5.QtGui import *
from PyQt5.QtGui import QCloseEvent, QKeyEvent
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtPrintSupport import *
import os
import sys
import json

json_path = ''

class HomeWindow(QWidget):
    
    # constructor
    def __init__(self, *args, **kwargs):
        super().__init__()

        # setting window geometry
        self.setGeometry(100, 100, 600, 400)

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("File Previews"))

        grid_layout = QGridLayout()
        layout.addLayout(grid_layout)

        self.pathfile_path = 'filepaths.txt'
        try:
            with open(self.pathfile_path, 'r') as f:
                self.filepaths = f.readlines()
        except FileNotFoundError:
            # Handle the case when the file doesn't exist
            self.filepaths = []
            print(self.pathfile_path + ' not found. So it is being created.')
            with open(self.pathfile_path, 'w') as f:
                pass


        self.show()

        
        self.default_dir = r'C:\Users\Karan\Documents\Avochoc\Note taking app\Default note location'


        self.json_path = r'C:\Users\Karan\Documents\Avochoc\Note taking app\quick-notes.json'


    def keyPressEvent(self, event):

        # Quit
        if event.key() == Qt.Key_Q:

            confirmation = QMessageBox.question(
                self, "Confirmation", "Are you sure you want to close the application?", 
                QMessageBox.Yes | QMessageBox.No)

            if confirmation == QMessageBox.Yes:
                QCoreApplication.instance().quit()

        # New
        elif event.key() == Qt.Key_N:
            self.note_window = NoteWindow(self.default_dir)
            self.close()

class NoteWindow(QMainWindow):

    # constructor
    def __init__(self, default_dir):
        super().__init__()
        self.setGeometry(100, 100, 600, 400)
        layout = QVBoxLayout()

        self.editor = QPlainTextEdit()
        fixedfont = QFontDatabase.systemFont(QFontDatabase.FixedFont)
        fixedfont.setPointSize(12)
        self.editor.setFont(fixedfont)

        # self.path holds the path of the currently open file.
        # If none, we haven't got a file open yet (or creating new).
        self.path = None

        layout.addWidget(self.editor)
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        self.status = QStatusBar()
        self.setStatusBar(self.status)


        # Save to default file location
        filename = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        self.path = os.path.join(default_dir, filename)
        self._save_to_path(self.path)

        # Save to json
        text = self.editor.toPlainText()
        with open(json_path, 'w') as f:
            


        # Adding home menu
        home_menu = self.menuBar().addMenu("&Home")
        home_action = QAction("&Home", self)
        home_action.setStatusTip("Home")
        home_action.triggered.connect(self.home)
        home_menu.addAction(home_action)


        # creating a file menu
        file_menu = self.menuBar().addMenu("&File")
        open_file_action = QAction("&Open file", self)
        open_file_action.setStatusTip("Open file")
        open_file_action.triggered.connect(self.file_open)
        file_menu.addAction(open_file_action)

        # similarly creating a save action
        save_file_action = QAction("&Save", self)
        save_file_action.setStatusTip("Save current page")
        save_file_action.triggered.connect(self.file_save)
        file_menu.addAction(save_file_action)

        # similarly creating Save As action
        saveas_file_action = QAction("Save &As", self)
        saveas_file_action.setStatusTip("Save current page to specified file")
        saveas_file_action.triggered.connect(self.file_saveas)
        file_menu.addAction(saveas_file_action)

        # for print action
        print_action = QAction("&Print", self)
        print_action.setStatusTip("Print current page")
        print_action.triggered.connect(self.file_print)
        file_menu.addAction(print_action)


        edit_menu = self.menuBar().addMenu("&Edit")

        undo_action = QAction("&Undo", self)
        undo_action.setStatusTip("Undo last change")
        undo_action.triggered.connect(self.editor.undo)
        edit_menu.addAction(undo_action)

        redo_action = QAction("&Redo", self)
        redo_action.setStatusTip("Redo last change")
        redo_action.triggered.connect(self.editor.redo)
        edit_menu.addAction(redo_action)

        cut_action = QAction("&Cut", self)
        cut_action.setStatusTip("Cut selected text")
        cut_action.triggered.connect(self.editor.cut)
        edit_menu.addAction(cut_action)

        copy_action = QAction("Cop&y", self)
        copy_action.setStatusTip("Copy selected text")
        copy_action.triggered.connect(self.editor.copy)
        edit_menu.addAction(copy_action)

        paste_action = QAction("&Paste", self)
        paste_action.setStatusTip("Paste from clipboard")
        paste_action.triggered.connect(self.editor.paste)
        edit_menu.addAction(paste_action)

        select_action = QAction("Select &all", self)
        select_action.setStatusTip("Select all text")
        select_action.triggered.connect(self.editor.selectAll)
        edit_menu.addAction(select_action)

        wrap_action = QAction("&Wrap text to window", self)
        wrap_action.setStatusTip("Check to wrap text to window")
        wrap_action.setCheckable(True)
        wrap_action.setChecked(True)
        wrap_action.triggered.connect(self.edit_toggle_wrap)
        edit_menu.addAction(wrap_action)

        self.update_title()
        self.show()


    def home(self):
        self.home_window = HomeWindow()

    def dialog_critical(self, s):
        dlg = QMessageBox(self)
        dlg.setText(s)
        dlg.setIcon(QMessageBox.Critical)
        dlg.show()

    def file_open(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open file", "", "Text documents (*.txt);All files (*.*)")
        if path:
            try:
                with open(path, 'rU') as f:
                    text = f.read()
            except Exception as e:
                self.dialog_critical(str(e))
            else:
                self.path = path
                self.editor.setPlainText(text)
                self.update_title()

    def file_save(self):
        if self.path is None:
            return self.file_saveas()
        self._save_to_path(self.path)

    def file_saveas(self):
        path, _ = QFileDialog.getSaveFileName(self, "Save file", "", "Text documents (*.txt);All files (*.*)")
        if not path:
            return
        self._save_to_path(path)

    def _save_to_path(self, path):
        text = self.editor.toPlainText()
        try:
            with open(path, 'w') as f:
                f.write(text)
        except Exception as e:
            self.dialog_critical(str(e))
        else:
            self.path = path
            self.update_title()

    def file_print(self):
        dlg = QPrintDialog()
        if dlg.exec_():
            self.editor.print_(dlg.printer())

    def update_title(self):
        self.setWindowTitle("%s - PyQt5 Notepad" % (os.path.basename(self.path) if self.path else "Untitled"))

    def edit_toggle_wrap(self):
        self.editor.setLineWrapMode(1 if self.editor.lineWrapMode() == 0 else 0)


# drivers code
if __name__ == '__main__':
    # creating PyQt5 application
    app = QApplication(sys.argv)

    # setting application name
    app.setApplicationName("PyQt5-Note")

    # creating a main window object
    window = HomeWindow()

    # loop
    app.exec_()
