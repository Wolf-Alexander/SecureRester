import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, 
                             QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox,
                             QListWidget, QMainWindow, QDialog, QDialogButtonBox)
from PyQt6.QtGui import QFont
from securerester import create_key, add, view 

class PasswordListDialog(QDialog):
    def __init__(self, passwords, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Password List")
        self.resize(300, 200)

        self.list_widget = QListWidget(self)
        for name, password in passwords:
            self.list_widget.addItem(f"Name: {name}, Password: {password}")

        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok, self)
        button_box.accepted.connect(self.accept)

        layout = QVBoxLayout(self)
        layout.addWidget(self.list_widget)
        layout.addWidget(button_box)

class PasswordManagerGUI(QMainWindow):  # Inherit from QMainWindow
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SecureRester")
        self.master_pwd = None 
        self.initUI()

    def initUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)  # Set central widget

        # Master Password Input
        self.master_pwd_label = QLabel("Enter Master Password:")
        self.master_pwd_input = QLineEdit()
        self.master_pwd_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.unlock_button = QPushButton("Unlock")
        self.unlock_button.clicked.connect(self.unlock)

        # Password Management Area
        self.pwd_mgmt_area = QWidget()
        self.pwd_mgmt_area.setVisible(False)

        # Add Password Section
        self.add_name_label = QLabel("Name:")
        self.add_name_input = QLineEdit()
        self.add_pwd_label = QLabel("Password:")
        self.add_pwd_input = QLineEdit()
        self.add_pwd_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.add_button = QPushButton("Add Password")
        self.add_button.clicked.connect(self.add_password)

        add_hbox = QHBoxLayout()
        add_hbox.addWidget(self.add_name_label)
        add_hbox.addWidget(self.add_name_input)
        add_hbox.addWidget(self.add_pwd_label)
        add_hbox.addWidget(self.add_pwd_input)
        add_hbox.addWidget(self.add_button)

        # View Passwords Section
        self.view_button = QPushButton("View Passwords")
        self.view_button.clicked.connect(self.view_passwords) 

        # Layout for Password Management Area
        pwd_mgmt_vbox = QVBoxLayout()
        pwd_mgmt_vbox.addLayout(add_hbox)
        pwd_mgmt_vbox.addWidget(self.view_button)
        self.pwd_mgmt_area.setLayout(pwd_mgmt_vbox)

        # Main Layout
        vbox = QVBoxLayout(central_widget)  # Layout on central widget
        vbox.addWidget(self.master_pwd_label)
        vbox.addWidget(self.master_pwd_input)
        vbox.addWidget(self.unlock_button)
        vbox.addWidget(self.pwd_mgmt_area)

        # Exit Button
        exit_action = self.menuBar().addAction("Exit")  # Add to menu bar
        exit_action.triggered.connect(self.close)

    def unlock(self):
        self.master_pwd = self.master_pwd_input.text()
        if self.master_pwd:
            self.pwd_mgmt_area.setVisible(True)
            self.master_pwd_input.clear() 
        else:
            QMessageBox.warning(self, "Error", "Please enter a master password.")

    def add_password(self):
        if self.master_pwd:
            name = self.add_name_input.text()
            pwd = self.add_pwd_input.text()
            add(self.master_pwd, name, pwd) 
            self.add_name_input.clear()
            self.add_pwd_input.clear()
        else:
            QMessageBox.warning(self, "Error", "Unlock with master password first.")

    def view_passwords(self):
        if self.master_pwd:
            passwords = view(self.master_pwd)
            if isinstance(passwords, str):  # Error message from view()
                QMessageBox.warning(self, "Error", passwords)
            else:
                dialog = PasswordListDialog(passwords, self)
                dialog.exec()
        else:
            QMessageBox.warning(self, "Error", "Unlock with master password first.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PasswordManagerGUI()
    window.show()
    sys.exit(app.exec())
