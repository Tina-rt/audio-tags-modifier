from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
import os
import eyed3


def getfilename(path_to_file):
    print(os.path.basename(path_to_file))


class App(QMainWindow):
    def __init__(self):
        super(App, self).__init__()
        self.mainLayout = QVBoxLayout()
        self.mainLayout.setSpacing(10)
        # self.mainLayout.setDirection()
        self.main_frame = QFrame(self)
        self.setCentralWidget(self.main_frame)
        self.main_frame.setLayout(self.mainLayout)

        self.file_layout = QHBoxLayout()
        self.mainLayout.addLayout(self.file_layout)

        self.label_files = QLabel('Files...')
        self.file_layout.addWidget(self.label_files)

        self.btn_open_file = QPushButton()
        self.btn_open_file.clicked.connect(self.open_file_dialog)
        self.btn_open_file.setText('Open files ..')
        self.file_layout.addWidget(self.btn_open_file)

        self.image_layout = QHBoxLayout()
        self.mainLayout.addLayout(self.image_layout)

        self.label_image_file = QLabel()

        self.image_layout.addWidget(self.label_image_file)

        self.btn_open_file_image = QPushButton()
        self.btn_open_file_image.setText('Choose a cover image')
        self.btn_open_file_image.clicked.connect(self.choose_image)
        self.image_layout.addWidget(self.btn_open_file_image)

        self.input_title = QLineEdit()
        self.input_title.setPlaceholderText("Music title")
        self.mainLayout.addWidget(self.input_title)

        self.input_album_title = QLineEdit()
        self.input_album_title.setPlaceholderText('Album title')
        self.mainLayout.addWidget(self.input_album_title)

        self.input_artist = QLineEdit()
        self.input_artist.setPlaceholderText('Artist')
        self.mainLayout.addWidget(self.input_artist)

        self.input_genre = QLineEdit()
        self.input_genre.setPlaceholderText('Genre')
        self.mainLayout.addWidget(self.input_genre)

        self.btn_submit = QPushButton()
        self.btn_submit.setText('Valider')
        self.btn_submit.clicked.connect(self.submit)
        self.mainLayout.addWidget(self.btn_submit)

        self.title = 'Mp3 modifier'
        self.image_cover = ''
        self.init_window()
        # self.createLayout()

        self.list_files = []

    def init_window(self):
        self.setWindowTitle(self.title)
        self.setMinimumWidth(600)
        self.setMinimumHeight(300)
        self.show()

    def choose_image(self):
        image_name = QFileDialog.getOpenFileName(self, 'Choose an image cover', 'C:\\', 'Image files (*.jpg *.png '
                                                                                        '*.jpeg)')
        # print(image_name)
        self.image_cover = image_name[0]
        self.label_image_file.setText(os.path.basename(self.image_cover))
        pix = QPixmap(self.image_cover)
        # pix.scaledToWidth()
        # self.label_image_file.setFixedWidth(60)
        # pix.scaledToWidth(60)
        pix.scaledToHeight(60)

        self.label_image_file.setPixmap(pix)

    def open_file_dialog(self):
        filenames = QFileDialog.getOpenFileNames(self, 'Open files', 'C:\\', 'Audio files(*.mp3 *.aac)')
        self.list_files = filenames[0]
        text = ', '.join([os.path.basename(filename) for filename in self.list_files])
        self.label_files.setText(text)

    def submit(self):
        artist = self.input_artist.text()
        album = self.input_album_title.text()
        genre = self.input_genre.text()
      

        if artist != '' or album != '' or genre != '':
            for file in self.list_files:
                audio_file = eyed3.load(file)

                audio_file.tag.artist = artist
                audio_file.tag.genre = genre
                audio_file.tag.album = album
                if self.image_cover != '':
                    with open(self.image_cover, 'rb') as image_file:
                        image_data = image_file.read()
                        print(audio_file.tag.images.set(3, image_data, 'image/jpg', u'cover'))
                audio_file.tag.save()

            QMessageBox.information(self, 'Done', 'Operation done successfully')


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = App()
    window.show()

    sys.exit(app.exec())
