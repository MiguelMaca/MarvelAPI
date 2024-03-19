# Con esta clase, se indica que elementos se necesitan del comic
# Para después el en comics_window mostrar la información de cada comic
class Comic:
    def __init__(
        self,
        name: str | None,
        description: str | None,
        image: str | None,
        isbn: int | None,
        date: str | None,
        characters: list | None,
        creators: list | None,
    ):
        self.name = name
        self.description = description
        self.image = image
        self.isbn = isbn
        self.date = date
        self.characters = characters
        self.creators = creators
