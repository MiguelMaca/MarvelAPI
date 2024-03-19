# Con esta clase, se indica que elementos se necesitan de los personajes
# Para despues el en characters_window mostrar la informacion de cada personaje
class Character:
    def __init__(
        self,
        name: str | None,
        image: str | None,
        description: str | None,
        comics: list | None,
        events: list | None,
    ):
        self.name = name
        self.image = image
        self.description = description
        self.comics = comics
        self.events = events
