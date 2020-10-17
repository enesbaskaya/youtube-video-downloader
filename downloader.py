from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sys
from pytube import YouTube

__author__ = "enesbaskaya"


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setUI()

    def setUI(self):
        self.settings()
        self.contentUI()
        self.show()

    # uygulama penceresi içerisinde görünecekler
    def contentUI(self):
        widget = QWidget()
        h_box = QHBoxLayout()
        v_box = QVBoxLayout()

        # içerikler
        title = QLabel("<center><h1>Youtube Video Downloader</center></h1>")
        title2 = QLabel("<center><h2>Enter link</center></h2>")
        self.link = QLineEdit()
        self.link.setPlaceholderText("https://www.youtube.com/enterurl")
        buttonDownload = QPushButton("Download", self)
        buttonDownload.clicked.connect(self.download)
        buttonDownload.setGeometry(50, 50, 50, 50)
        v_box.addWidget(title)

        # içeriklerin atanması
        v_box.addWidget(title)
        h_box.addWidget(title2)
        h_box.addWidget(self.link)
        v_box.addLayout(h_box)
        v_box.addWidget(buttonDownload)
        widget.setLayout(v_box)
        self.setCentralWidget(widget)

    # pencere ve icon ayarları
    def settings(self):
        # pencere başlık ve icon
        self.setWindowTitle("Youtube DownLoader")
        self.setWindowIcon(QIcon("eb.png"))

        # pencere boyutlandırma
        self.setGeometry(250, 250, 400, 80)

    # indirme butonu aksiyon
    def download(self):
        title = "Download Manager"
        contentText = "Download Complete!"
        url = self.link.text()
        # video kalilesi
        res = "1080p"
        video = YouTube(url).streams.filter(res=res).first().download()
        if (YouTube):
            QMessageBox.information(self, title, contentText)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec())
