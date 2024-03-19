from urllib.request import urlretrieve

from PyQt6 import QtGui, QtCore
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

# Al momento de presionar el boton de detalles, se necesita la información que se mostrara
from character import Character


# Clase para mostrar información del personaje al presionar el botón de detalles
class CharacterWindow(QMainWindow):
    def __init__(self, character: Character):
        super().__init__()
        # Características de la ventana
        # Se indica que es la ventana de detalles con su respectiva geometria
        self.setWindowTitle("Detalles")
        self.setGeometry(100, 100, 100, 100)
        # Se añade el ícono de marvel
        self.setWindowIcon(QIcon("marvel_icon.png"))
        self.center()

        # Se agregan los layout base
        self.general = QVBoxLayout()
        # Layouts comics
        self.comics_general = QVBoxLayout()
        self.comics_layout1 = QVBoxLayout()
        self.comics_layout2 = QVBoxLayout()
        self.comics_buttons = QHBoxLayout()
        # Layouts events
        self.events_general = QVBoxLayout()
        self.events_layout1 = QVBoxLayout()
        self.events_layout2 = QVBoxLayout()
        # Información general
        self.info_general = QVBoxLayout()

        # Información del personaje
        self.name = character.name
        self.description = character.description
        self.comics = character.comics
        self.events = character.events
        self.image = character.image

        # Se hace el proceso para mostrar la imagen del personaje
        url = self.image
        urlretrieve(url, "../image.jpg")
        self.img = QLabel(self)
        # Se ajusta el tamaño de imagen
        self.img.setPixmap(
            QPixmap("../image.jpg").scaled(400, 600, Qt.AspectRatioMode.KeepAspectRatio)
        )
        self.img.setScaledContents(True)
        self.general.addWidget(self.img)

        # Se agrega la información al layout
        self.name_label = QLabel(self.name)
        self.name_label.setFont(QFont("Arial", 20))
        self.name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # Se agrega boton de avanzar y regresar
        self.avanzar_button = QPushButton("Avanzar")
        self.avanzar_button.clicked.connect(self.avanzar)

        self.retroceder_button = QPushButton("Retroceder")
        self.retroceder_button.clicked.connect(self.retroceder)

        # El contador sirve para saber si hay comics o no
        contador_comics = 0

        # Título indicando los comics de los personajes
        self.principal_comic = QLabel("COMICS")
        self.principal_comic.setFont(QFont("Arial", 15))
        # Se añade el título con su respectivo estilo a comics_general para poder mostrarlo luego
        self.comics_general.addWidget(self.principal_comic)
        # Un for donde recorrerá comic por comic
        for comic in self.comics:
            nombre_comic = comic["name"]
            contador_comics += 1
            # Se añade el contador - nombre del comic
            comic_label = QLabel(f"{contador_comics} - {nombre_comic}")
            # Mientras el contador de comics no sea mayor a 10, ejecute lo siguiente
            if contador_comics < 10:
                self.comics_layout1.addWidget(comic_label)
                # Se añade comics_layout1 a comics_general
                self.comics_general.addLayout(self.comics_layout1)
            # Si el contador de comics es 0, indica que no hay comics y que muestre que no hay comics para mostrar
            elif contador_comics == 0:
                comics_nulos = QLabel("No tiene comics")
                self.comics_general.addWidget(comics_nulos)
                break
            # Si hay mas de 10 comics, se añaden el resto al layout2 y se muestran los botones de avanzar y regresar
            elif contador_comics >= 10:
                self.comics_layout2.addWidget(comic_label)
                self.comics_buttons.addWidget(self.retroceder_button)
                self.comics_buttons.addWidget(self.avanzar_button)
            self.comics_general.addLayout(self.comics_buttons)

        # Método para obtener los eventos
        contador_events = 0
        # Título indicando los eventos
        self.principal_event = QLabel("EVENTOS")
        self.principal_event.setFont(QFont("Arial", 15))
        # Se añadel el titulo a events_general para poder mostrarlo luego
        self.events_general.addWidget(self.principal_event)

        # Un for donde recorrera evento por evento
        try :
            for event in self.events:
                nombre_event = event["name"]
                # Un label que muestre el contador y el nombre del evento
                event_label = QLabel(f"{contador_events} - {nombre_event}")

                # Si la longitud de los comics es mayor a 10 y el contador es menor a 10
                # Añada los eventos al layout 1
                if len(self.comics) > 10 and contador_events < 10:
                    contador_events += 1
                    self.events_layout1.addWidget(event_label)
                    # Se añade layout1 a events_general para luego mostrarlo
                    self.events_general.addLayout(self.events_layout1)

                else:
                    # De lo contrario qeu se añadan al layout2
                    contador_events += 1
                    self.comics_layout2.addWidget(event_label)

        except Exception:
            self.events_nulos = QLabel("No tiene eventos")
            self.events_nulos.setStyleSheet("background-color: orange")
            self.events_nulos.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.events_general.addWidget(self.events_nulos)

        # Título de descripcion con su respectivo estilo
        self.principal_description = QLabel("DESCRIPTION")
        self.principal_description.setFont(QFont("Arial", 15))

        # Si la descripción es Vacia '', mensaje sin descripción
        if self.description == "":
            self.description_label = QLabel("Sin descripción")
            # Se le añade un color
            self.description_label.setStyleSheet("background-color: red")
            self.description_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        else:
            # De lo contrario muestre la descripción
            self.description_label = QLabel(f"DESCRIPCIÓN: {self.description}")
        self.back = QPushButton("Regresar")
        self.back.clicked.connect(self.go_back)
        self.back.setStyleSheet("QPushButton::hover" "{" "background-color : red;" "}")
        # Se añaden todos a info_general
        self.info_general.addWidget(self.name_label)
        self.info_general.addLayout(self.events_general)
        self.info_general.addWidget(self.principal_description)
        self.info_general.addWidget(self.description_label)
        self.info_general.addLayout(self.comics_general)
        self.info_general.addWidget(self.back)
        # Se añade info_general a general para poder mostrarlo
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

    # Regresar a ventana anterior
    def go_back(self):
        self.close()

    # Función para cargar el programa
    def load_UI(self):
        self.show()

    # Función para avanzar de página
    def avanzar(self):
        self.comics_general.addLayout(self.comics_layout2)
        self.show()

    # Función para retroceder página
    def retroceder(self):
        self.comics_general.addLayout(self.comics_layout1)
        self.show()
