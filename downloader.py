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

        # içerikler
        title = QLabel("<b>Enter link</b>")
        self.link = QLineEdit()
        self.link.setPlaceholderText("https://www.youtube.com/enterurl")
        buttonDownload = QPushButton("Download", self)
        buttonDownload.clicked.connect(self.download)

        # içeriklerin atanması
        h_box.addWidget(title)
        h_box.addWidget(self.link)
        h_box.addWidget(buttonDownload)
        widget.setLayout(h_box)
        self.setCentralWidget(widget)

    # pencere ve icon ayarları
    def settings(self):
        # pencere başlık ve icon
        self.setWindowTitle("Youtube DownLoader")
        self.setWindowIcon(QIcon("eb.png"))

        # pencere boyutlandırma
        self.setGeometry(250, 250, 600, 100)
        self.setMaximumSize(800, 120)
        self.setMinimumSize(500, 80)

    # indirme butonu aksiyon
    def download(self):
        url = self.link.text()
        # video kalilesi
        res1080p = "1080p"
        YouTube(url).streams.filter(res=res1080p).first().download()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    pencere = Window()
    sys.exit(app.exec())
