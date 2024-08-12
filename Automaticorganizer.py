import os
import shutil
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QMessageBox ,QSizePolicy
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt, QSize

class FileOrganizerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Automatic File')
        self.setGeometry(100, 100, 800, 400)  # Default size

        # Central widget and layout
        central_widget = QWidget()  
        layout = QVBoxLayout(central_widget)

        # Application logo
        self.logo_label = QLabel(self)
        self.logo_pixmap = QPixmap('logo.png')
        self.logo_label.setPixmap(self.logo_pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.logo_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.logo_label)

        # Application name label with bold font
        title_text = '<b>Automatic File Organizer</b>'
        self.title_label = QLabel(title_text, self)
        self.title_label.setFont(QFont('Arial', 24, QFont.Bold))
        self.title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.title_label)

        title_text = '<br><font size="4" color="#666666">Amr Elwany</font>'
        self.title_label = QLabel(title_text, self)
        self.title_label.setFont(QFont('Arial', 8, QFont.Bold))
        self.title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.title_label)

        # Background image label
        self.background_label = QLabel(self)
        self.background_pixmap = QPixmap('folder_icon.png')
        self.background_label.setPixmap(self.background_pixmap.scaled(800, 400, Qt.IgnoreAspectRatio, Qt.SmoothTransformation))
        self.background_label.setGeometry(0, 0, 800, 400)
        self.background_label.lower()  # Place it behind other widgets

        # Select button
        self.select_button = QPushButton('Select Folder', self)
        self.select_button.setStyleSheet('background-color: #4CAF50; color: white; font-size: 16px; padding: 10px; border-radius: 5px;')
        self.select_button.clicked.connect(self.select_folder)
        layout.addWidget(self.select_button)

        self.setCentralWidget(central_widget)

        # Set the size policies for responsive resizing
        self.logo_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.title_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.select_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

    def select_folder(self):
        path = QFileDialog.getExistingDirectory(self, 'Select Folder')
        if path:
            self.organize_files(path)

    def organize_files(self, path):
        files = os.listdir(path)

        # Get unique extensions
        unique_extensions = set()
        no_extension_files = []

        for filename in files:
            if '.' in filename:  # Check if there's an extension
                extension = filename.split('.')[-1]
                unique_extensions.add(extension)
            else:
                no_extension_files.append(filename)

        # Create folder names and make directories
        created_folders = []

        for extension in unique_extensions:
            folder_name = f"{extension} files"
            folder_path = os.path.join(path, folder_name)
            
            if not os.path.exists(folder_path):
                os.mkdir(folder_path)
                created_folders.append(folder_name)

        # Move files into corresponding folders
        for filename in files:
            if '.' in filename:  # Check if there's an extension
                extension = filename.split('.')[-1]
                folder_name = f"{extension} files"
                folder_path = os.path.join(path, folder_name)
                
                # Move the file to the corresponding folder
                src_file_path = os.path.join(path, filename)
                dest_file_path = os.path.join(folder_path, filename)
                shutil.move(src_file_path, dest_file_path)

        # Print number of folders created and their names
        if created_folders:
            msg = f"Number of folders created: {len(created_folders)}\n"
            msg += "Folders created:\n" + "\n".join(f"- {folder}" for folder in created_folders)
            QMessageBox.information(self, "Folders Created", msg)
        else:
            QMessageBox.information(self, "No New Folders", "No new folders were created.")

        # Additional message for files without extensions
        if no_extension_files:
            no_ext_files = "\n".join(no_extension_files)
            QMessageBox.information(self, "Files Without Extensions", 
                                    "The following files have no extension and do not need to be organized:\n" +
                                    no_ext_files)
        else:
            QMessageBox.information(self, "Organization Complete", 
                                    "All files have been organized into folders based on their extensions.")

if __name__ == '__main__':
    app = QApplication([])
    window = FileOrganizerApp()
    window.show()
    app.exec_()
