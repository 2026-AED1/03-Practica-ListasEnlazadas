# lista_simple.py
# La lista SIMPLEMENTE enlazada del repaso (bloque 2), ya completa.
# No hay que modificarla: sirve de punto de comparacion en comparativa.py.
#
# Solo tiene puntero al SIGUIENTE. Por eso todo lo que necesita "mirar hacia
# atras" obliga a recorrer desde la cabeza:
#   delete_last  -> O(n): hay que encontrar el penultimo
#   delete_node  -> O(n): hay que encontrar el anterior del nodo
#   recorrer hacia atras -> no hay forma directa


class Nodo:
    __slots__ = ("dato", "siguiente")

    def __init__(self, dato):
        self.dato = dato
        self.siguiente = None


class ListaSimple:
    def __init__(self, iterable=None):
        self.cabeza = None
        self.cola = None          # con puntero a cola, insert_last es O(1)
        self.tamano = 0
        if iterable is not None:
            for dato in iterable:
                self.insert_last(dato)

    def __len__(self):
        return self.tamano

    def __iter__(self):
        actual = self.cabeza
        while actual is not None:
            yield actual.dato
            actual = actual.siguiente

    def __getitem__(self, pos):
        # O(n): hay que seguir pos enlaces desde la cabeza.
        if not 0 <= pos < self.tamano:
            raise IndexError("posicion fuera de rango")
        actual = self.cabeza
        for _ in range(pos):
            actual = actual.siguiente
        return actual.dato

    def buscar(self, dato):
        actual = self.cabeza
        while actual is not None and actual.dato != dato:
            actual = actual.siguiente
        return actual

    def insert_first(self, dato):                       # O(1)
        nuevo = Nodo(dato)
        nuevo.siguiente = self.cabeza
        self.cabeza = nuevo
        if self.cola is None:
            self.cola = nuevo
        self.tamano += 1
        return nuevo

    def insert_last(self, dato):                        # O(1) gracias a cola
        nuevo = Nodo(dato)
        if self.cola is None:
            self.cabeza = self.cola = nuevo
        else:
            self.cola.siguiente = nuevo
            self.cola = nuevo
        self.tamano += 1
        return nuevo

    def delete_first(self):                             # O(1)
        if self.cabeza is None:
            raise IndexError("delete_first sobre una lista vacia")
        nodo = self.cabeza
        self.cabeza = nodo.siguiente
        if self.cabeza is None:
            self.cola = None
        self.tamano -= 1
        return nodo.dato

    def delete_last(self):                              # O(n)
        if self.cola is None:
            raise IndexError("delete_last sobre una lista vacia")
        if self.cabeza is self.cola:
            return self.delete_first()
        penultimo = self.cabeza
        while penultimo.siguiente is not self.cola:     # <- el recorrido
            penultimo = penultimo.siguiente
        dato = self.cola.dato
        penultimo.siguiente = None
        self.cola = penultimo
        self.tamano -= 1
        return dato

    def delete_node(self, nodo):                        # O(n)
        if nodo is self.cabeza:
            return self.delete_first()
        anterior = self.cabeza
        while anterior.siguiente is not nodo:           # <- el recorrido
            anterior = anterior.siguiente
        anterior.siguiente = nodo.siguiente
        if nodo is self.cola:
            self.cola = anterior
        self.tamano -= 1
        return nodo.dato
