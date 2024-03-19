from urllib.request import urlretrieve
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QFont
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton
from character import Character
from windows.character_window import CharacterWindow


# Clase para mostrar la información de cada personaje junto con el boton de detalles
class CharacterWidget(QWidget):
    def __init__(self, character: Character):
        super().__init__()
        self.info_personaje = CharacterWindow(character)

        # Se agregan los layout base
        layout1 = QHBoxLayout()

        # Se hace el proceso para mostrar la imagen del personaje
        url = character.image
        urlretrieve(url, "../image.jpg")
        self.img = QLabel(self)
        # Se ajusta el tamaño a la imagen y se mejora su calidad
        self.img.setPixmap(
            QPixmap("../image.jpg").scaled(100, 150, Qt.AspectRatioMode.KeepAspectRatio)
        )
        self.img.setScaledContents(True)
        # Se ingresa la imagen en el layout1
        layout1.addWidget(self.img)

        # Creación de layout2
        layout2 = QVBoxLayout()
        # Se muestra el nombre al inicio con su respectivo estilo
        self.name = QLabel(character.name)
        self.name.setFont(QFont("Bebas", 12))
        # Creación de botón detalles
        self.info_button = QPushButton("Detalles")
        self.info_button.clicked.connect(self.character_info)
        # Color a botón
        self.info_button.setStyleSheet(
            "QPushButton::hover" "{" "background-color : lightblue;" "}"
        )
        # Se añade al layout2 el nombre y su respectiva informacion (Detalles)
        layout2.addWidget(self.name)
        layout2.addWidget(self.info_button)

        # Se agrega el layout2 a la infromacion del widget para que se muestre y
        # Se agrega la informacion del widget al layout1 para que se muestre
        # Todo_en la ventana
        info_widget = QWidget()
        info_widget.setLayout(layout2)
        layout1.addWidget(info_widget)

        self.setLayout(layout1)
        self.close()

    def character_info(self):
        self.info_personaje.load_UI()
