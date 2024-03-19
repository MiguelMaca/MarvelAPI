from typing import TypeVar, Generic

# Se guarda el tipo de variable genérico
T = TypeVar("T")


class Node(Generic[T]):
    def __init__(self, data: T):
        self.data: T = data
        # El siguiente es de tipo nodo o nulo
        self.next: Node | None = None
