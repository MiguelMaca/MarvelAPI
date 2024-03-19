import hashlib
import math
import time
from tkinter import messagebox

import requests
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtWidgets import (
    QMainWindow,
    QPushButton,
    QWidget,
    QHBoxLayout,
    QLabel,
    QVBoxLayout,
    QGridLayout,
    QLineEdit,
)

# Con este import se obtiene el nombre del personaje, descripcion, etc.
from character import Character
from list.circular_list import CircularList

# Este import sirve para generar el boton de detalles en la ventana de personajes
from widget.character_widget import CharacterWidget


# Variables globales
timestamp = time.time()
# Se requieren las llaves para poder acceder a la API de Marvel
public_key = "3294e8e263f834283ac7532f36181086"
secret_key = "8d4b1b1b700b516bc3f63278901a7ffc0d587992"
access = f"{timestamp}{secret_key}{public_key}"

# Variables de control
total_pages_characters = 0
total_pages_comics = 0

# Caracteristicas de busqueda
page = 0
limit = 10

# Pasa la cadena a bytes
ultra_secret = hashlib.md5(access.encode())


class CharactersWindow(QMainWindow):
    def __init__(self):
        self.characters_list: CircularList[Character] = CircularList()
        super().__init__()

        # Características de la ventana
        self.setWindowTitle("CATÁLOGO DE SUPERHEROES")
        # Geometria de la ventana
        self.setGeometry(100, 100, 400, 100)
        # Se añade el icono de marvel a la esquina de la ventana
        self.setWindowIcon(QIcon("marvel_icon.png"))
        self.center()

        # Se genera el texto de la ventana con su respectivo tamaño y letra
        self.characters_label = QLabel("Listado de personajes")
        self.characters_label.setFont(QFont("Arial", 20))
        # Se centra el characters_label
        self.characters_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # Color de mi fondo
        self.characters_label.setStyleSheet("background-color: lightpink")

        # Se genera una caja de texto donde se podra ingresar el personaje que se desea buscar
        self.nombre_a_buscar = QLineEdit()
        self.buscar_por_nombre = QPushButton("Buscar por nombre")
        # Se manda la funcion buscar a al boton 'buscar_por_nombre'
        self.buscar_por_nombre.clicked.connect(self.buscar)

        # Botón de avanzar
        self.avanzar_button = QPushButton("Avanzar")
        # Se manda la funcion avanzar al boton para que ejecute la accion
        self.avanzar_button.clicked.connect(self.avanzar)
        # Color al botón
        self.avanzar_button.setStyleSheet(
            "QPushButton::hover" "{" "background-color : lightgreen;" "}"
        )

        # Boton para regresar
        self.regresar_button = QPushButton("Regresar")
        # Se manda la funcion regresar al boton para que ejecute la accion de regresar
        self.regresar_button.clicked.connect(self.regresar)
        # Color al botón
        self.regresar_button.setStyleSheet(
            "QPushButton::hover" "{" "background-color : orange;" "}"
        )

        # Boton para regresar al menú
        self.menu_button = QPushButton("Ir al menú")
        # Se conecta con la funcion menu para que este tenga su respectiva accion
        self.menu_button.clicked.connect(self.menu)
        # Color al boton de menu
        self.menu_button.setStyleSheet(
            "QPushButton::hover" "{" "background-color : red;" "}"
        )

        # Se hace la interfaz de posición para los botones
        self.general = QVBoxLayout()
        self.busqueda = QHBoxLayout()
        self.botones = QHBoxLayout()
        self.characters_grid = QGridLayout()

        # Se agregan los botones a la interfaz con self.general
        self.general.addWidget(self.characters_label)
        # Se añade la funcion busqueda a general
        self.busqueda.addWidget(self.nombre_a_buscar)
        self.busqueda.addWidget(self.buscar_por_nombre)
        self.general.addLayout(self.busqueda)
        # Se añade botones a general
        self.botones.addWidget(self.regresar_button)
        self.botones.addWidget(self.avanzar_button)
        self.general.addLayout(self.characters_grid)

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

    # Función para regresar al menú principal
    def menu(self):
        global page
        page = 0
        self.clear()
        self.close()

    # Funcion para avanzar de página
    def avanzar(self):
        global page
        self.clear()
        # Las páginas aumentaran en uno al momento de cambiar
        page += 1
        # Se muestra mensaje de espera
        messagebox.showinfo(
            message="Se están buscando los personajes, sea paciente por favor.",
            title="Buscador",
        )
        self.characters_list_info()

    # Funcion para retroceder de página
    def regresar(self):
        global page
        self.clear()
        if page == 0:
            # Se muestra mensaje de espera
            messagebox.showinfo(
                message="No se puede retroceder a la página anterior",
                title="Alerta",
            )
            page = 0
        else:
            # La página disminuirá en uno
            page -= 1
        self.characters_list_info()

    # Funcion para obtener los personajes donde se envia la page y el limite de
    # Los personajes que se mostrarán
    def get_characters(self, page, limit):
        global total_pages_characters

        # Se accede a la URL para obtener los personajes
        endpoint = "https://gateway.marvel.com/v1/public/"
        resource = "characters"
        # Ingreso de paramatros para autentificar el acceso a Marvel
        params = {
            "apikey": public_key,
            "ts": timestamp,
            "hash": ultra_secret.hexdigest(),
            "limit": limit,
            # Se utiliza para realaizar la paginación
            "offset": page * limit,
        }

        # Se encapsula la respuesta del servidor ingresar el endpoint y el tipo de evento que se necesita
        # Se ingresa los parametros y se iguala a los datos de autentificación
        response = requests.get(f"{endpoint}{resource}", params=params)

        # Menú para personajes de Marvel
        data = response.json()["data"]
        total = data["total"]
        total_pages_characters = math.ceil(total / limit)
        characters = data["results"]
        # Se retornan los personajes para que los nuestre
        return characters

    # Obtener la lista de caracteres con un límite de 10
    def characters_list_info(self):
        self.characters_list.clear()
        # Se define la ruta de access y el recurso a solicitar
        endpoint = "https://gateway.marvel.com/v1/public/"
        # Se accede a los personajes
        resource = "characters"
        characters = self.get_characters(page, limit)
        # Tratar de obtener la información de cada personaje
        # Se encapsula la información los errores
        # y las fallas de la API
        try:
            contador_x = 0
            contador_y = 0
            for item in characters:
                # Se importo Characters para poder obtener la siguiente informacion
                character = Character(
                    item["name"],
                    item["thumbnail"]["path"] + ".jpg",
                    item["description"],
                    item["comics"]["items"],
                    list(item["events"]["items"]),
                )
                self.characters_list.append(character)

            for character in self.characters_list.transversal():
                character_widget = CharacterWidget(character)
                # Agregar el widget a la lista de los personajes
                if contador_x > 4:
                    contador_y += 1
                    contador_x = 0
                self.characters_grid.addWidget(character_widget, contador_x, contador_y)
                contador_x += 1
                # Se añade el listado de canciones al layout principal
            self.general.addLayout(self.characters_grid)
        except Exception as e:
            print(e)
        self.mostrar_pagina()
        self.show()

    # Información para un personaje
    def get_character_info(id):
        global total_pages_characters
        endpoint = "https://gateway.marvel.com/v1/public/characters/"
        characterId = id
        # Ingreso de parametros para autentificar el acceso a Marvel
        params = {
            "apikey": public_key,
            "ts": timestamp,
            "hash": ultra_secret.hexdigest(),
            # Se utiliza para realaizar la paginación
        }

        # Se encapsula la respuesta del servidor ingresar el endpoint y el tipo de evento que se necesita
        # Se ingresa los parametros y se iguala a los datos de autentificación
        response = requests.get(f"{endpoint}{characterId}", params=params)

        # Se necesitan los datos para la respuesta
        data = response.json()["data"]
        personaje = data["results"]

        return personaje

    # Funcion par limpiar pantala
    def clear(self):
        # Se limpia el listado después de mostrarlo
        self.characters_list.clear()
        # Se limpia el layout utilizado en los personajes
        for i in reversed(range(self.characters_grid.count())):
            self.characters_grid.itemAt(i).widget().setParent(None)

    # Funcion para mostrar la pagina actual
    def mostrar_pagina(self):
        global page
        page_label = QLabel(f"Página: {page + 1} de {total_pages_characters}")
        # Se le añade estilo al QLabel
        page_label.setFont(QFont("Arial", 10))
        page_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.characters_grid.addWidget(page_label, 5, 0)
        self.general.addLayout(self.botones)
        self.general.addWidget(self.menu_button)

    def load_UI(self):
        self.show()
        self.characters_list_info()

    def get_character_info(self, character_id):
        global total_pages_comics
        endpoint = "https://gateway.marvel.com/v1/public/characters/"
        characterId = character_id
        # Ingreso de parametros para autentificar el acceso a Marvel
        params = {
            "apikey": public_key,
            "ts": timestamp,
            "hash": ultra_secret.hexdigest(),
            # Se utiliza para realizar la paginación
        }

        # Se encapsula la respuesta del servidor ingresar el endpoint y el tipo de evento que se necesita
        # Se ingresa los parametros y se iguala a los datos de autentificación
        response = requests.get(f"{endpoint}{characterId}", params=params)

        # Menú para personajes de Marvel
        data = response.json()["data"]
        character = data["results"]

        return character

    # Funcion para obtener el id del personaje
    def obtener_character_id(self, nombre) -> int:
        characters = self.get_characters(page, limit)
        for character in characters:
            if character["name"] == nombre:
                return character["id"]

    # Funcion para buscar al personaje deseado
    def buscar(self):
        nombre = self.nombre_a_buscar.text()
        self.nombre_a_buscar.setText("")
        character_id = self.obtener_character_id(nombre)
        # Si no existe el personaje deseado mostrar lo siguiente
        if character_id is None:
            messagebox.showinfo(
                message="No se encuentra el personaje con ese nombre",
                title="Alerta",
            )
        else:
            self.clear()
            # Si existe el personaje deseado mostrar el siguiente mensaje
            messagebox.showinfo(
                message="Se está buscando el personaje, tenga paciencia",
                title="Buscador",
            )
            character_obtenido = self.get_character_info(character_id)
            # Si existe el personaje mostrar toda su informacion
            for item in character_obtenido:
                character = Character(
                    item["name"],
                    item["thumbnail"]["path"] + ".jpg",
                    item["description"],
                    item["comics"]["items"],
                    list(item["events"]["items"]),
                )
                character_widget = CharacterWidget(character)
                self.characters_grid.addWidget(character_widget, 0, 0)
            # Se añade el listado de canciones al layout principal
            self.general.addLayout(self.characters_grid)
            self.mostrar_pagina()
            self.show()
