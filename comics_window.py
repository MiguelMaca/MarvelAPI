import hashlib
import math
import time
from tkinter import messagebox

import requests
from PyQt6.QtCore import Qt, QSize
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

# Se necesita este import para tener el nombre, descripcion, isbn, etc.
from comic import Comic
from list.circular_list import CircularList

# Este import sirve para generar el boton de detalles en la ventana de comics
from widget.comic_widget import ComicWidget

# Variables globales
timestamp = time.time()
# Se requiere de las llaves para poder acceder a la API de Marvel
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


class ComicsWindow(QMainWindow):
    def __init__(self):
        self.comics_list: CircularList[Comic] = CircularList()
        super().__init__()
        # Características de la ventana
        self.setWindowTitle("CATÁLOGO DE COMICS")
        # geometria de la ventana
        self.setGeometry(100, 100, 400, 100)
        # Se le añade imagen a la esquina de la ventana
        self.setWindowIcon(QIcon("marvel_icon.png"))
        self.center()

        # Se genera el texto de listado de comics con su respectivo tamaño y letra
        self.comics_label = QLabel("Listado de comics")
        self.comics_label.setFont(QFont("Arial", 20))
        # Se centra nuestro comics_label
        self.comics_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # Se le asigna un color
        self.comics_label.setStyleSheet("background-color: lightpink")

        # Se genera una una caja de texto para buscar los comics
        self.nombre_a_buscar = QLineEdit()
        self.buscar_por_nombre = QPushButton("Buscar por nombre o fecha")
        # Se conecta el boton a la funcion buscar
        self.buscar_por_nombre.clicked.connect(self.buscar)

        # Botón de avanzar
        self.avanzar_button = QPushButton("Avanzar")
        # Se conecta el boton de avanzar a la funcion avanzar para cambiar de página
        self.avanzar_button.clicked.connect(self.avanzar)
        # Se le asigna color al botón
        self.avanzar_button.setStyleSheet(
            "QPushButton::hover" "{" "background-color : lightgreen;" "}"
        )

        # Boton para regresar
        self.regresar_button = QPushButton("Regresar")
        # Se conecta el boton de regresar a la funcion regresar para retroceder de página
        self.regresar_button.clicked.connect(self.regresar)
        # Se le asigna color al botón
        self.regresar_button.setStyleSheet(
            "QPushButton::hover" "{" "background-color : orange;" "}"
        )

        # Se genera botón para poder regresar al menú
        self.menu_button = QPushButton("Ir al menú")
        # Se conecta a la función menu para que ejecute la acción
        self.menu_button.clicked.connect(self.menu)
        # Se le asigna el color al botón
        self.menu_button.setStyleSheet(
            "QPushButton::hover" "{" "background-color : red;" "}"
        )

        # Se genera la posicion que tendran los botones
        self.general = QVBoxLayout()
        self.busqueda = QHBoxLayout()
        self.botones = QHBoxLayout()
        self.comics_grid = QGridLayout()

        # Se agregan los botones al general
        self.general.addWidget(self.comics_label)
        # Se agrega la busqueda al general que contiene las acciones
        self.busqueda.addWidget(self.nombre_a_buscar)
        self.busqueda.addWidget(self.buscar_por_nombre)
        self.general.addLayout(self.busqueda)
        # Se agregan los botones al general que contiene las acciones
        self.botones.addWidget(self.regresar_button)
        self.botones.addWidget(self.avanzar_button)
        self.general.addLayout(self.comics_grid)

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
        # Se cierra la ventana de comics
        self.close()

    # Función para avanzar de página
    def avanzar(self):
        global page
        self.clear()
        # La pagina se irá aumentando cada vez que se presione el botón de avanzar
        page += 1
        # Se muestra mensaje de espera
        messagebox.showinfo(
            message="Se está buscando el comic, sea paciente por favor.",
            title="Buscador",
        )
        self.comics_list_info()

    # Función para regresar de página
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
            # La página dismunuirá
            page -= 1
        self.comics_list_info()

    # Funcion para obtener comics, donde se envía la página y el límite de comics que se muestran
    def get_comics(self, page, limit):
        global total_pages_comics

        # Se accede a la URL
        endpoint = "https://gateway.marvel.com/v1/public/"
        # Se necesita acceder a 'comics' para obtener la informcación
        resource = "comics"
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
        total_pages_comics = math.ceil(total / limit)
        comics = data["results"]

        return comics

    # Función para obtener información de comics
    def comics_list_info(self):
        self.comics_list.clear()
        # Se define la ruta de access y el recurso a solicitar
        endpoint = "https://gateway.marvel.com/v1/public/"
        resource = "comics"
        comics = self.get_comics(page, limit)
        # Tratar de obtener la información de cada comic
        # Se encapsula la información los errores
        # y las fallas de la API
        try:
            contador_x = 0
            contador_y = 0
            for item in comics:
                # Se importa Comic para obtener la siguiente información
                comic = Comic(
                    item["title"],
                    item["description"],
                    item["thumbnail"]["path"] + ".jpg",
                    item["isbn"],
                    item["dates"][0]["date"],
                    [item["characters"]],
                    [item["creators"]],
                )
                self.comics_list.append(comic)
            for comic in self.comics_list.transversal():

                comic_widget = ComicWidget(comic)
                # Agregar el widget a la lista de personajes

                if contador_x > 4:
                    contador_y += 1
                    contador_x = 0
                self.comics_grid.addWidget(comic_widget, contador_x, contador_y)
                contador_x += 1
                # Se añade el listado de canciones al layout principal
            self.general.addLayout(self.comics_grid)
        except Exception as e:
            print(e)
        self.mostrar_pagina()
        self.show()

    # Función para obtener la información del comic
    def get_comic_info(comics_id):
        global total_pages_comics
        endpoint = "https://gateway.marvel.com/v1/public/comics/"
        comicId = id
        # Ingreso de parametros para autentificar el acceso a Marvel
        params = {
            "apikey": public_key,
            "ts": timestamp,
            "hash": ultra_secret.hexdigest(),
            # Se utiliza para realizar la paginación
        }

        # Se encapsula la respuesta del servidor ingresar el endpoint y el tipo de evento que se necesita
        # Se ingresa los parametros y se iguala a los datos de autentificación
        response = requests.get(f"{endpoint}{comicId}", params=params)

        # Se necesitan los datos como respuesta
        data = response.json()["data"]
        comic = data["results"]

        return comic

    def clear(self):
        # Se limpia el listado después de mostrarlo
        self.comics_list.clear()
        # Se limpia el layout utilizado en las canciones
        for i in reversed(range(self.comics_grid.count())):
            self.comics_grid.itemAt(i).widget().setParent(None)

    # Funcion para mostrar la página actual
    def mostrar_pagina(self):
        global page
        page_label = QLabel(f"Página: {page + 1} de {total_pages_comics}")
        page_label.setFont(QFont("Arial", 10))
        page_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.comics_grid.addWidget(page_label, 5, 0)
        self.general.addLayout(self.botones)
        self.general.addWidget(self.menu_button)

    def load_UI(self):
        self.show()
        self.comics_list_info()

    def get_comic_info(self, id):
        global total_pages_characters
        endpoint = "https://gateway.marvel.com/v1/public/comics/"
        comicsid = id
        # Ingreso de paramatros para autentificar el acceso a Marvel
        params = {
            "apikey": public_key,
            "ts": timestamp,
            "hash": ultra_secret.hexdigest(),
            # Se utiliza para realizar la paginación
        }

        # Se encapsula la respuesta del servidor ingresar el endpoint y el tipo de evento que se necesita
        # Se ingresa los parametros y se iguala a los datos de autentificación
        response = requests.get(f"{endpoint}{comicsid}", params=params)

        # Menú para comics de Marvel
        data = response.json()["data"]
        comic = data["results"]

        return comic

    # Funcion para obtener el id del comic
    def obtener_comic_id(self, nombre) -> int:
        comics = self.get_comics(page, limit)
        for comic in comics:
            if comic["title"] == nombre:
                return comic["id"]

    # Función para buscar un comic en especifico
    def buscar(self):
        nombre = self.nombre_a_buscar.text()
        self.nombre_a_buscar.setText("")
        comic_id = self.obtener_comic_id(nombre)
        # Si no exisete el comic que se quiere obtener entonces
        if comic_id is None:
            messagebox.showinfo(
                message="No se encuentra el comic con ese nombre",
                title="Alerta",
            )

        # Mostrar mensaje para indicar que se esta localizando el comic solicitado
        else:
            self.clear()
            messagebox.showinfo(
                message="Se está buscando el comic, tenga paciencia",
                title="Buscador",
            )
            # Se necesita de nuevo la informacion del comic si el buscado existe
            comic_obtenido = self.get_comic_info(comic_id)
            # Si el comic deseado existe, mostrar toda su informacion
            for item in comic_obtenido:
                comic = Comic(
                    item["title"],
                    item["description"],
                    item["thumbnail"]["path"] + ".jpg",
                    item["isbn"],
                    item["dates"][0]["date"],
                    list(item["characters"]),
                    list(item["creators"]),
                )
                comic_widget = ComicWidget(comic)
                self.comics_grid.addWidget(comic_widget, 0, 0)
            # Se añade el listado de canciones al layout principal
            self.general.addLayout(self.comics_grid)
            self.mostrar_pagina()
            self.show()
