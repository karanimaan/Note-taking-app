from datetime import datetime
import os
from PyQt5.QtGui import *
from PyQt5.QtGui import QCloseEvent, QKeyEvent
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtPrintSupport import *
import sys
from tinydb import TinyDB, Query
from PyQt5 import QtCore
import PyQt5

if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
    PyQt5.QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
    PyQt5.QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)


json_filename = 'quick-notes.json'


class NotePreviewWidget(QFrame):
    def __init__(self, note):
        super().__init__()

        layout = QVBoxLayout(self)

        title = note.get('title', 'Untitled')
        content = note.get('content', '')

        if title != '':
            # QLabel for title
            title_label = QLabel(title)
            title_label.setAlignment(Qt.AlignCenter)
            title_label.setStyleSheet('font-weight: bold; font-size: 12pt')
            layout.addWidget(title_label)

        # QLabel for preview
        preview_label = QLabel(content)
        preview_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(preview_label)

        
        self.setLayout(layout)
        self.setStyleSheet("""
                        NotePreviewWidget {
                            background-color: #F0F0F0; /* Set your desired background color */
                            border: 1px solid #CCCCCC; /* Set a border for distinction */
                            margin: 5px; /* Add some margin */
                            padding: 5px; /* Add padding to content */
                        }
                    """)
        
        self.enter_shortcut = QShortcut(QKeySequence("Return"), self)



class HomeWindow(QWidget):
    
    # constructor
    def __init__(self):
        super().__init__()

        # self.showMaximized()

        hint_lbl = QLabel('Press "n" to create a new note')
        hint_lbl.setStyleSheet('font-size: 10pt')
        hint_lbl.setAlignment(Qt.AlignCenter)

        vertical_layout = QVBoxLayout(self)
        vertical_layout.addWidget(hint_lbl)
            

        if not os.path.isfile(json_filename):   # if json file doesn't exist 
            with open(json_filename, 'w') as db:    # create file
                pass

        else:

            with TinyDB(json_filename) as db:
                notes = db.all()

            list_widget = QListWidget(self)
            for index, note in enumerate(notes):
                note_preview = NotePreviewWidget(note)
                note_preview.enter_shortcut.activated.connect(lambda: self.open_note(note))

                item = QListWidgetItem(list_widget)
                item.setSizeHint(note_preview.sizeHint())

                list_widget.addItem(item)   
                list_widget.setItemWidget(item, note_preview)


            vertical_layout.addWidget(list_widget) 


        self.n_shortcut = QShortcut(QKeySequence("n"), self)
        self.n_shortcut.activated.connect(self.new_note)

        self.q_shortcut = QShortcut(QKeySequence("q"), self)
        self.q_shortcut.activated.connect(self.quit)

   


        # self.setFocus()
        self.show()

    @pyqtSlot()
    def quit(self):
        confirmation = QMessageBox.question(self, "Confirmation", "Are you sure you want to close the application?", QMessageBox.Yes | QMessageBox.No)
        if confirmation == QMessageBox.Yes:
            QCoreApplication.instance().quit()


    @pyqtSlot()
    def open_note(self, note):
        title = note.get('title', 'Untitled')
        content = note.get('content', '')
        self.note_window = NoteWindow(title, content)
        self.close()


    @pyqtSlot()
    def new_note(self):
        self.note_window = NoteWindow()
        self.close()

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
            self.note_window = NoteWindow()
            self.close()


class NoteWindow(QMainWindow):

    def __init__(self, title=None, content=None):
        super().__init__()

        # self.showMaximized()
        
        self.title = title
        self.content = content
        

        self.title_bar = QLineEdit()
        self.title_bar.setStyleSheet('font-size: 22pt')

        self.editor = QPlainTextEdit()
        self.editor.setStyleSheet('font-size: 18pt')

        
        layout = QVBoxLayout()
        layout.addWidget(self.title_bar)
        layout.addWidget(self.editor)

        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)
        self.status = QStatusBar()
        self.setStatusBar(self.status)


        if self.title is None:

            self.date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')    # date created (id for record)            

        else:

            # Load json entry
            self.setWindowTitle(f"{self.title} - QuickNote")
            self.title_bar.setText(self.title)
            self.editor.setPlainText(self.content)

        self.add_to_menuBar()
        self.editor.setFocus()
        self.show()

            
    def keyPressEvent(self, a0: QKeyEvent) -> None:
        if a0.key() == Qt.Key_Escape:
            self.go_home()
        return super().keyPressEvent(a0)

    def add_to_menuBar(self):

        # Adding home menu

        home_action = QAction("&Home", self)
        home_action.setStatusTip("Home")
        home_action.triggered.connect(self.go_home)

        home_menu = self.menuBar().addMenu("&Home")
        home_menu.triggered.connect(self.go_home)
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



    def closeEvent(self, a0: QCloseEvent):
        # save content to json
        Note = Query()
        title = self.title_bar.text()
        content = self.editor.toPlainText()
        if content != '':
            with TinyDB(json_filename) as db:
                if db.search(Note.date == self.date) == []:
                    db.insert({
                        'title': title,
                        'content': content,
                        'date': self.date    # date created
                    })
                else:
                    db.update({'title': title, 'content': content}, Note.date == self.date)
        super().closeEvent(a0)
            


    def go_home(self):
        self.close()
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

    def edit_toggle_wrap(self):
        self.editor.setLineWrapMode(1 if self.editor.lineWrapMode() == 0 else 0)


# drivers code
if __name__ == '__main__':
    # creating PyQt5 application
    app = QApplication(sys.argv)

    # setting application name
    app.setApplicationName("QuickNote")

    # creating a main window object
    window = HomeWindow()

    # loop
    app.exec_()
