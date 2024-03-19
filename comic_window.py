from urllib.request import urlretrieve

from PyQt6 import QtGui
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QPixmap, QFont
from PyQt6.QtWidgets import (
    QLabel,
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QLabel,
    QVBoxLayout,
    QPushButton,
)

# Al momento de presionar el boton de detalles, se necesita la informacion que se mostrará
from comic import Comic


# Clase paa mostrar infromacion del comic al presionar el boton de detalles
class ComicWindow(QMainWindow):
    def __init__(self, comic: Comic):
        super().__init__()
        # Características de la ventana
        # Se indica que es la ventana de detalles con su respectiva geometria
        self.setWindowTitle("Detalles")
        self.setGeometry(100, 100, 100, 100)
        # Se añade el icono de marvel
        self.setWindowIcon(QIcon("marvel_icon.png"))
        self.center()

        # Se agregan los layout base
        self.general = QVBoxLayout()
        # Layouts creators
        self.creators_general = QVBoxLayout()
        self.creators_layout1 = QVBoxLayout()
        self.creators_layout2 = QVBoxLayout()
        self.creators_buttons = QHBoxLayout()
        # Layouts characters
        self.characters_general = QVBoxLayout()
        self.characters_layout1 = QVBoxLayout()
        self.characters_layout2 = QVBoxLayout()
        self.characters_buttons = QHBoxLayout()
        # información general
        self.info_general = QVBoxLayout()

        # Información del comic
        self.name = comic.name
        self.description = comic.description
        self.isbn = comic.isbn
        self.date = comic.date
        self.characters = comic.characters
        self.creators = comic.creators
        self.image = comic.image

        # Se hace el proceso para mostrar la imagen del comic
        url = self.image
        urlretrieve(url, "../image.jpg")
        self.img = QLabel(self)
        # Se ajusta el tamaño a la imagen
        self.img.setPixmap(
            QPixmap("../image.jpg").scaled(200, 300, Qt.AspectRatioMode.KeepAspectRatio)
        )
        self.img.setScaledContents(True)
        self.general.addWidget(self.img)

        # Se agrega el nombre al layout
        self.name_label = QLabel(self.name)
        self.name_label.setFont(QFont("Arial", 20))
        self.name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Se agrega el isbn al layout
        self.isbn_label = QLabel(self.isbn)
        self.isbn_label.setFont(QFont("Arial", 15))
        self.isbn_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Se añaden los botones para avanzar y retroceder
        self.avanzar_button = QPushButton("Avanzar")
        self.avanzar_button.clicked.connect(self.avanzar)

        self.retroceder_button = QPushButton("Retroceder")
        self.retroceder_button.clicked.connect(self.retroceder)

        # El contador sirve para saber si hay personajes o no
        contador_characters = 0

        # Titulo indicando los personajes de los comics
        self.principal_characters = QLabel("CHARACTERS")
        self.principal_characters.setFont(QFont("Arial", 15))
        # Se añade el titulo con su respectivo estilo a character_general para poder mostrarlo luego
        self.characters_general.addWidget(self.principal_characters)

        # Un for donde recorre character por character
        try:
            for characters in self.characters:
                nombre_character = characters["items"]
                # Se añade el contador - nombre del personaje
                character_label = QLabel(f"{contador_characters} - {nombre_character}")

                # Si existe 1 personaje o 9 personajes, que se agreguen al primer layout
                if 10 > contador_characters > 0:
                    contador_characters += 1
                    self.characters_layout1.addWidget(character_label)

                    self.characters_general.addLayout(self.characters_layout1)

                # Si hay mas de 10 personajes, se añaden al segundo layout y se muestran
                # Los botones para avanzar o retroceder
                elif contador_characters >= 10:
                    contador_characters += 1
                    self.characters_layout2.addWidget(character_label)
                    self.characters_buttons.addWidget(self.retroceder_button)
                    self.characters_buttons.addWidget(self.avanzar_button)
                self.characters_general.addLayout(self.characters_buttons)
        except Exception:
            self.no_characters = QLabel("No tiene personajes")
            self.no_characters.setStyleSheet("background-color: orange")
            self.no_characters.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.characters_general.addWidget(self.no_characters)
        # Se añaden los creadores y su contador
        contador_creators = 0

        # Título indicando los personajes de los comics
        self.principal_creators = QLabel("CREATORS")
        self.principal_creators.setFont(QFont("Arial", 15))
        self.creators_general.addWidget(self.principal_creators)

        # Un for donde recorrera creator por creator
        try:
            for creators in self.creators:
                nombre_creator = creators["items"]

                # Se añade el contador - nombre del creador
                creator_label = QLabel(f"{contador_creators} - {nombre_creator}")

                # Si existe 1 creador o 9 creadores, que se agreguen al primer layout
                if 10 > contador_creators > 0:
                    contador_creators += 1
                    self.creators_layout1.addWidget(creator_label)
                    self.creators_general.addLayout(self.creators_layout1)

                # Si hay mas de 10 creadores, que se añadan al segundo layout y aparezcan los botones de avanzar y regresar
                elif contador_creators >= 10:
                    contador_creators += 1
                    self.creators_layout2.addWidget(creator_label)
                    self.creators_buttons.addWidget(self.retroceder_button)
                    self.creators_buttons.addWidget(self.avanzar_button)
                self.creators_general.addLayout(self.creators_buttons)

        except Exception:
            self.no_creators = QLabel("No tiene creadores")
            self.no_creators.setStyleSheet("background-color: lightblue")
            self.no_creators.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.creators_general.addWidget(self.no_creators)
        # Título para indicar el ISBN
        self.principal_isbn = QLabel("ISBN")
        self.principal_isbn.setFont(QFont("Arial", 15))

        # Título para indicar la descripción del comic
        self.principal_description = QLabel("DESCRIPTION")
        self.principal_description.setFont(QFont("Arial", 15))

        # Si no existe el isbn que indique que no hay isbn
        if self.isbn == "":
            self.isbn_label = QLabel("Sin isbn")
            self.isbn_label.setStyleSheet("background-color: lightgreen")
            self.isbn_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # De lo contrario que lo muestre
        else:
            self.isbn_label = QLabel(self.isbn)

        # Si no existe descripción que indique que no hay descripción del comic
        if self.description == "":
            self.description_label = QLabel("Sin descripción")
            self.description_label.setStyleSheet("background-color: red")
            self.description_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # De lo contrario que me muestre la descripción
        else:
            self.description_label = QLabel(self.description)
        self.back = QPushButton("Regresar")
        self.back.clicked.connect(self.go_back)
        self.back.setStyleSheet("QPushButton::hover" "{" "background-color : red;" "}")

        # Se añade la información a la informacion general
        self.info_general.addWidget(self.name_label)
        self.info_general.addWidget(self.principal_isbn)
        self.info_general.addWidget(self.isbn_label)
        self.info_general.addWidget(self.principal_description)
        self.info_general.addWidget(self.description_label)
        self.info_general.addLayout(self.characters_general)
        self.info_general.addLayout(self.creators_general)
        self.info_general.addWidget(self.back)

        # Se añade la infromación general al general
        self.general.addLayout(self.info_general)
        self.widget = QWidget()
        self.widget.setLayout(self.general)

        # Se muestra el widget
        self.setCentralWidget(self.widget)

    # Función para centrar la ventana
    def center(self):
        qr = self.frameGeometry()
        cp = self.screen().availableGeometry().center()

        qr.moveCenter(cp)
        self.move(qr.topLeft())

    # Función para regresar
    def go_back(self):
        self.close()

    # Esta función ejecutará el programa
    def load_UI(self):
        self.show()

    # Función para avanzar de página
    def avanzar(self):
        self.characters_general.addLayout(self.characters_layout2)
        self.show()

    # Función para retroceder o regresar de página
    def retroceder(self):
        self.characters_general.addLayout(self.characters_layout1)
        self.show()
