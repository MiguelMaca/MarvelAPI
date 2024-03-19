from PyQt6.QtGui import QFont, QIcon, QPixmap
from PyQt6.QtWidgets import QMainWindow, QPushButton, QWidget, QHBoxLayout

# Se necesita la informacion de los personajes y comics para la ventana principal
from windows.characters_window import CharactersWindow
from windows.comics_window import ComicsWindow


class MenuWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Llamamos a los personaes y a los comics
        self.comics_window = ComicsWindow()
        self.characters_window = CharactersWindow()
        self.comics_window.close()
        self.characters_window.close()

        # Características de la ventana
        self.setWindowTitle("CATÁLOGO DE SUPERHEROES")
        self.setWindowIcon(QIcon("marvel_icon.png"))
        # Tamaño de la ventana
        self.setGeometry(50, 200, 200, 50)
        self.center()

        # Se generan los botones y el texto que debe tener cada uno
        # También se les modifica el tamaño a cada uno
        # Función para comics
        self.comics_button = QPushButton("Comics")
        # Se conecta el boton para acceder a los comics
        self.comics_button.clicked.connect(self.acceder_a_comics)

        # Se le asigna el tamaño a nuestro botón
        self.comics_button.setFixedSize(150, 75)
        self.comics_button.setFont(QFont("Arial", 15))
        # Función para cambiar el estilo del botón
        self.comics_button.setStyleSheet(
            "QPushButton::hover" "{" "background-color : red;" "}"
        )
        self.comics_button.clicked.connect(self.acceder_a_comics)

        # Funciones de personajes
        self.personajes_button = QPushButton("Personajes")
        self.personajes_button.clicked.connect(self.acceder_a_personajes)

        # Se le asigna el tamaño a el botón
        self.personajes_button.setFixedSize(150, 75)
        self.personajes_button.setFont(QFont("Arial", 15))
        # Función para cambiar el estilo del botón
        self.personajes_button.setStyleSheet(
            "QPushButton::hover" "{" "background-color : lightgreen;" "}"
        )
        self.personajes_button.clicked.connect(self.acceder_a_personajes)

        # Se hace la interfaz de posición para los botones
        self.layout = QHBoxLayout()

        # Se agregan los botones a la interfaz
        self.layout.addWidget(self.comics_button)
        self.layout.addWidget(self.personajes_button)
        # Se agregan márgenes a la interfaz
        self.layout.setSpacing(10)

        widget = QWidget()
        # Al widget se le  agrega el self.layout
        widget.setLayout(self.layout)

        # Se muestra el widget
        self.setCentralWidget(widget)

    # Función para centrar la ventana
    def center(self):
        qr = self.frameGeometry()
        cp = self.screen().availableGeometry().center()

        qr.moveCenter(cp)
        self.move(qr.topLeft())

    # Función para mostrar la ventana de comics
    def acceder_a_comics(self):
        self.comics_window.load_UI()

    # Función para mostrar la ventana de personajes
    def acceder_a_personajes(self):
        self.characters_window.load_UI()
