from list.node import Node
from typing import TypeVar, Generic

# Se guarda el tipo de variable genérico
T = TypeVar("T")


class CircularList(Generic[T]):
    def __init__(self):
        self.head: Node | None = None
        self.tail: Node | None = None
        self.size = 0

    # Eliminar al inicio
    def shift(self):
        # La lista está vacía
        if self.is_empty():
            raise ValueError("No hay datos por eliminar")

        # Ya solo hay un elemento en la lista
        elif self.head == self.tail:
            current = self.head
            self.head = None
            self.tail = None
            self.size -= 1
            return current
        # Se elimina normalmente
        else:
            current = self.head
            self.head = current.next
            self.tail.next = self.head
            current.next = None
            self.tail.next = self.head
            self.size -= 1
            return current

    # Posición en específico
    def insert_at(self, data: T, pos: int):
        new_node = Node(data)
        if self.is_empty():
            self.head = new_node
            self.tail = new_node
            self.size += 1
        else:
            if pos == 0:
                self.prepend(data)
            elif pos == self.size:
                self.append(data)
            else:
                previous = self.find_at(pos - 1)
                new_node.next = previous.next
                previous.next = new_node
                self.size += 1

    # Se elimina al final
    def pop(self) -> T:
        current = self.tail

        if self.is_empty():
            raise Exception("No se puede eliminar más valores")

        # Se comprueba que haya más de un elemento en la lista
        elif self.head == self.tail:
            self.head = None
            self.tail = None
            current.next = None
            self.size = 0
            return current

        # se toma en cuenta el último elemento
        else:
            prev = self.find_at(self.size - 2)
            self.tail = prev
            prev.next = None
            self.size -= 1
            return current

    # Agregar al inicio
    def prepend(self, data: T) -> None:
        new_node = Node(data)
        # La lista está vacía(mover dos punteros)
        if self.is_empty():
            self.head = new_node
            self.tail = new_node
        else:
            new_node.next = self.head
            self.head = new_node

        self.tail.next = self.head
        self.size += 1

    # Agregar al final
    def append(self, data: T):
        new_node = Node(data)
        # La lista está vacía(mover dos punteros)
        if self.is_empty():
            self.head = new_node
        else:
            self.tail.next = new_node

        self.tail = new_node
        self.tail.next = self.head
        self.size += 1

    # Buscar un elemento en la lista
    def find_by(self, data: T) -> Node:
        current = self.head
        if self.is_empty():
            raise ValueError("La lista está vacía")
        else:
            # Se busca mientras no sea la cola
            while current is not None:
                # Si es igual a la data que retorne el current
                if current.data == data:
                    return current
                else:
                    current = current.next

                # Al ser igual que la cabeza es porque ya se recorrió
                if current == self.head:
                    break
            raise ValueError(f"El dato {data} no está en la lista")

    # Buscar según la posición
    def find_at(self, index: int) -> Node:
        current = self.head
        i = 0
        while current is not None:
            if i == index:
                return current
            elif self.tail.next == current.next:
                break
            else:
                current = current.next
                i += 1

        raise Exception("La posición no existe")

    # Recorrer la lista
    def transversal(self) -> list:
        result = []
        # Se comprueba que la lista esté vacía
        if self.is_empty():
            print("La lista está vacía")
        else:
            # Se recorre la lista
            current = self.head
            while current is not self.tail:
                result.append(current.data)
                current = current.next
            result.append(current.data)
        return result

    # Limpiar la lista
    def clear(self):
        self.head = None
        self.tail = None
        self.size = 0

    def is_empty(self):
        return self.head is None and self.tail is None
