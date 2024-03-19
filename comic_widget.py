from urllib.request import urlretrieve

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QFont
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton
from comic import Comic
from windows.comic_window import ComicWindow


# Clase para mostrar la información de cada comic junto con el boton de detalles
class ComicWidget(QWidget):
    def __init__(self, comic: Comic):
        super().__init__()
        self.info_comic = ComicWindow(comic)

        # Se agregan los layout base
        layout1 = QHBoxLayout()

        # Se hace el proceso para mostrar la imagen del comic
        url = comic.image
        urlretrieve(url, "../image.jpg")
        self.img = QLabel(self)
        # Se ajusta el tamaño a la imagen y se mejora su calidad
        self.img.setPixmap(
            QPixmap("../image.jpg").scaled(50, 75, Qt.AspectRatioMode.KeepAspectRatio)
        )
        self.img.setScaledContents(True)
        # Se ingresa la imagen en el layout1
        layout1.addWidget(self.img)

        # Creación de layout2
        layout2 = QVBoxLayout()
        # Se muestra el nombre al inicio con su respectivo estilo
        self.name = QLabel(comic.name)
        self.name.setFont(QFont("Bebas", 12))
        # Creación de botón detalles
        self.info_button = QPushButton("Detalles")
        self.info_button.clicked.connect(self.comic_info)
        # Color a botón
        self.info_button.setStyleSheet(
            "QPushButton::hover" "{" "background-color : lightblue;" "}"
        )
        self.date = QLabel(comic.date)
        # Se añade al layout2 el nombre, la fecha y su respectiva informacion (Detalles)
        layout2.addWidget(self.name)
        layout2.addWidget(self.date)
        layout2.addWidget(self.info_button)

        # Se agrega el layout2 a la infromacion del widget para que se muestre y
        # Se agrega la informacion del widget al layout1 para que se muestre
        # Todo_en la ventana
        info_widget = QWidget()
        info_widget.setLayout(layout2)
        layout1.addWidget(info_widget)

        self.setLayout(layout1)

    def comic_info(self):
        self.info_comic.load_UI()
