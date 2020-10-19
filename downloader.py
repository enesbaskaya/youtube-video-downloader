from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from pytube import YouTube
from threading import Thread
import os, datetime, sys


__author__ = "enesbaskaya"


# some global values
windowIcon = "eb.png"
videoURL = ''           # to store the link of the video
videoMetadata = []      # to store the video details
user_dir = os.path.expanduser("~") + "\\"       # the "C:\Users\<user>" folder
video_dir = 'Downloads\\YouTube Video Downloader\\' # get the absolute path of destination folder (inside the Downloads)




def get_video(url):
    """get the video from the url and store the data in videoMetadata"""
    yt = YouTube(url)   # video object
    
    # video metadata
    title = yt.title
    duration = str(datetime.timedelta(seconds = yt.length))
    views = ("{:,}".format(yt.views))

    # store the data now
    videoMetadata.append(title)
    videoMetadata.append(duration)
    videoMetadata.append(views)



def download_video():
    """Download the desired video in the specified directory using a new thread"""
    try:
        try: os.mkdir(user_dir + video_dir) # create new folder if not present
        except Exception as e: pass         # generates error if already present

        yt = YouTube(videoURL)                      # get the object
        ys = yt.streams.get_highest_resolution()    # get the highest resolution video
        ys.download(user_dir + video_dir)           # download at the specified directory

    except Exception as e: print("Error in 'download_video' function\n", e)   # print if any error occurs
    



class Window(QMainWindow):
    """Main application class"""
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
        self.link.setPlaceholderText("https://www.youtu.be/video-id")
        buttonDownload = QPushButton("Download", self)
        buttonDownload.clicked.connect(self.download)
        buttonDownload.setShortcut("Return")    # Shortcut for button
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
        """Initiate the process when user clicks on the button"""
        global videoURL
        url = videoURL = self.link.text()   # store the link of the video user entered
        
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
            
        except Exception as e: print("Error in 'download' function:\n", e)



    def confirm_download(self, status):
        """Start Download only if confirmed"""
        if status.text().lower() == "ok":
            # start video downloading in a new thread
            d = Thread(target=download_video)
            d.start()
            if d.is_alive(): print('Downloading... Please Wait')
            else: print('An Error occured')
            d.join()


            try:
                # After download, show confirmation box along with video location
                contentText = "Download Complete!"
                alert_box = QMessageBox()
                alert_box.setIcon(QMessageBox.Information)
                alert_box.setText(contentText)
                alert_box.setInformativeText("Downloaded at:-\n{0}".format(video_dir))
                alert_box.setWindowTitle("YouTube Video Downloader")
                alert_box.addButton(QPushButton('Open Folder'), QMessageBox.YesRole)
                alert_box.addButton(QPushButton('OK'), QMessageBox.NoRole)
                alert_box.setWindowIcon(QIcon(windowIcon))
                alert_box.buttonClicked.connect(self.open_downloads)
                alert_box.exec_()
            except Exception as e: print("Error in 'confirm_download' function", e)

        else: print("Cancelled")
                
        global videoMetadata
        videoMetadata = []      # reset the video data after use



    def open_downloads(self, status):
        """Open the download folder of videos"""
        if status.text().lower() != "ok": os.startfile(user_dir + video_dir)
    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec())
