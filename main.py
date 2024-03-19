# Inicio de proyecto de superhéroes
# Se importan las librerías necesarias para el proyecto.
import sys
from PyQt6.QtWidgets import QApplication
from windows.menu_window import MenuWindow


# Variables globales se necesitarán para ejecutar el proyecto
app = QApplication(sys.argv)
menu = MenuWindow()


# El menú se muestra
def load_window():
    menu.show()


# Bloque de código main
def main():
    load_window()
    sys.exit(app.exec())


# Ejecución del proyecto
main()
