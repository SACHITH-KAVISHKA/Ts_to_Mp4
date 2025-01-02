import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QFileDialog, QProgressBar, QVBoxLayout
)
from PyQt5.QtCore import Qt
import subprocess


class VideoConverter(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.filePath = None

    def initUI(self):
        # Window settings
        self.setWindowTitle("TS to MP4 Converter")
        self.setGeometry(300, 200, 400, 200)

        # Layout and widgets
        layout = QVBoxLayout()

        self.label = QLabel("Select a TS file to convert:", self)
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)

        self.progressBar = QProgressBar(self)
        self.progressBar.setAlignment(Qt.AlignCenter)
        self.progressBar.setValue(0)
        layout.addWidget(self.progressBar)

        self.browseButton = QPushButton("Browse", self)
        self.browseButton.clicked.connect(self.browseFile)
        layout.addWidget(self.browseButton)

        self.convertButton = QPushButton("Convert", self)
        self.convertButton.setEnabled(False)
        self.convertButton.clicked.connect(self.convertFile)
        layout.addWidget(self.convertButton)

        self.statusLabel = QLabel("", self)
        self.statusLabel.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.statusLabel)

        self.setLayout(layout)

    def browseFile(self):
        file, _ = QFileDialog.getOpenFileName(self, "Open TS File", "", "TS Files (*.ts)")
        if file:
            self.filePath = file
            self.label.setText(f"Selected: {os.path.basename(file)}")
            self.convertButton.setEnabled(True)

    def convertFile(self):
        if not self.filePath:
            self.statusLabel.setText("No file selected!")
            return

        self.progressBar.setValue(10)
        output_file = self.filePath.replace(".ts", ".mp4")

        command = ["ffmpeg", "-i", self.filePath, "-c", "copy", output_file]

        try:
            self.statusLabel.setText("Converting...")
            self.progressBar.setValue(50)

            # Run FFmpeg command
            subprocess.run(command, check=True)

            self.progressBar.setValue(100)
            self.statusLabel.setText(f"Conversion completed: {os.path.basename(output_file)}")
        except subprocess.CalledProcessError as e:
            self.statusLabel.setText("Conversion failed!")
            print(f"Error: {e}")
        except Exception as e:
            self.statusLabel.setText("An unexpected error occurred!")
            print(f"Error: {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    converter = VideoConverter()
    converter.show()
    sys.exit(app.exec_())
