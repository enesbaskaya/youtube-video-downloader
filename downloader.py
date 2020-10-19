from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sys
from pytube import YouTube
import datetime
from threading import Thread
import os
import logging

__author__ = "enesbaskaya"


# some global values
windowIcon = "eb.png"
videoURL = ''
videoMetadata = []
video_dir = os.path.expanduser("~") + '\\Downloads\\YouTube Video Downloader\\' # get the absolute path of destination folder



def get_video(url):
    """get the video from the url and return the data"""
    # video object
    yt = YouTube(url)
    # video metadata
    title = yt.title
    duration = str(datetime.timedelta(seconds = yt.length))
    views = ("{:,}".format(yt.views))
    videoMetadata.append(title)
    videoMetadata.append(duration)
    videoMetadata.append(views)



def download_video():
    """Download the desired video in the specified directory"""
    try:
        try: os.mkdir(video_dir)          # create a temporary folder for PyMediaPlayer if not present
        except Exception as e: pass     # generates error if already present
    
        yt = YouTube(videoURL)
        ys = yt.streams.get_highest_resolution()
        #ys.download(video_dir)
    except Exception as e: print("Error:", e)
    


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
        enterLintText = QLabel("<center><h2>Enter link</center></h2>")
        self.link = QLineEdit()
        self.link.setPlaceholderText("https://www.youtube.com/enterurl")
        buttonDownload = QPushButton("Download", self)
        buttonDownload.clicked.connect(self.download)
        buttonDownload.setGeometry(50, 50, 50, 50)
        v_box.addWidget(title)

        # içeriklerin atanması
        v_box.addWidget(title)
        h_box.addWidget(enterLintText)
        h_box.addWidget(self.link)
        v_box.addLayout(h_box)
        v_box.addWidget(buttonDownload)
        widget.setLayout(v_box)
        
        self.setCentralWidget(widget)

    # pencere ve icon ayarları
    def settings(self):
        # pencere başlık ve icon
        windowTitle = "Youtube DownLoader"
        self.setWindowTitle(windowTitle)
        self.setWindowIcon(QIcon(windowIcon))

        # pencere boyutlandırma
        self.setGeometry(250, 250, 400, 80)


    # indirme butonu aksiyon
    def download(self):
        global videoURL
        url = videoURL = self.link.text()
        
        try:
            # start video searching in a new thread
            t = Thread(target=get_video, args =(url,))
            t.start()
            if t.is_alive():print('Processing')
            else: print('An Error occured')
            t.join()

            # get the metadata of the video
            title, duration, views = videoMetadata


            # confirmation message box details
            conf_box = QMessageBox()
            conf_box.setIcon(QMessageBox.Information)
            conf_box.setText("Do you want to download this video?")
            conf_box.setInformativeText("Title: {0}\nDuration: {1}\nViews: {2}".format(title,duration,views))
            conf_box.setWindowTitle("YouTube Video Downloader")
            conf_box.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            conf_box.setWindowIcon(QIcon(windowIcon))
            conf_box.buttonClicked.connect(self.confirm_download)
            conf_box.exec_()
            
        except Exception as e: print(e)



    # Start downlaod only if confirmed
    def confirm_download(self, status):
        """Download only if confirmed"""
        if status.text().lower() == "ok":
            # start video downloading in a new thread
            d = Thread(target=download_video)
            d.start()
            
            if d.is_alive(): print('Downloading')
            else: print('An Error occured')
            d.join()
            
            # After its downloaded
            contentText = "Download Complete!"
            alert_box = QMessageBox()
            alert_box.setIcon(QMessageBox.Information)
            alert_box.setTitle(contentText)
            alert_box.setInformativeText("Downloaded at: ", video_dir)
            alert_box.setWindowTitle("YouTube Video Downloader")
            alert_box.setStandardButtons(QMessageBox.Ok)
            alert_box.setWindowIcon(QIcon(windowIcon))
            alert_box.exec_()

        
        print(videoMetadata)
        videoMetadata.clear()
        print(videoMetadata)

        
            
    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec())
