# lista_doble.py
# Practica 3 - Lista doblemente enlazada.
#
# Objetivo: implementar la lista doble con puntero a cabeza, puntero a cola y
# contador de tamano, y hacer que se use como una secuencia de Python:
# len(l), for x in l, reversed(l), x in l, print(l).
#
# Hay que completar los metodos marcados con TODO (cada uno lanza ahora
# NotImplementedError) y sustituir cada "O(?)" por el coste que consigue tu
# implementacion. Lo que ya esta escrito no se toca: los tests y el juez
# dependen de los nombres (cabeza, cola, tamano, dato, siguiente, anterior).
#
# Orden de trabajo (Parte 1 y 2, en clase) y tests de cada paso:
#   1. insert_last, __reversed__          -> test_lista_doble.PruebasInsercion
#   2. insert_before, insert_after        -> test_lista_doble.PruebasInsercionRelativa
#   3. delete_node, delete_first/last     -> test_lista_doble.PruebasBorrado
#                                            test_lista_doble.PruebaContraList
#   4. es_palindromo                      -> test_lista_doble.PruebasPalindromo
# Ampliacion (opcional): reverse, intercalar, rotar -> PruebasReverse,
#   PruebasIntercalar, PruebasRotar (se saltan mientras no los hagas).
#
# Ejecutar los tests:
#   python3 -m unittest -v test_lista_doble
#
# Juez (DOMjudge, problema "Lista doble"): se sube ESTE fichero tal cual.
# Pruebalo antes con:  python3 lista_doble.py < ejemplo_lista.txt


class NodoDoble:
    # __slots__: cada nodo solo tiene hueco para estos tres campos, sin
    # diccionario de atributos. Ahorra mucha memoria.
    __slots__ = ("dato", "siguiente", "anterior")

    def __init__(self, dato):
        self.dato = dato
        self.siguiente = None
        self.anterior = None


class ListaDoble:
    # --- Invariante de la representacion ---------------------------------
    #  tamano >= 0
    #  tamano == 0  <=>  cabeza is None  <=>  cola is None
    #  si tamano > 0:
    #    cabeza.anterior is None  y  cola.siguiente is None
    #    partiendo de cabeza y siguiendo .siguiente se visitan exactamente
    #    tamano nodos y el ultimo es cola
    #    para cada nodo x que no es la cabeza: x.anterior.siguiente is x
    #
    # TODAS las operaciones deben dejarlo cierto al terminar (mientras
    # trabajan pueden romperlo). Los tests lo comprueban despues de cada
    # llamada con invariante_correcto().
    # ---------------------------------------------------------------------

    def __init__(self, iterable=None):
        self.cabeza = None
        self.cola = None
        self.tamano = 0
        if iterable is not None:                 # ListaDoble([1, 2, 3])
            for dato in iterable:
                self.insert_last(dato)

    # --- Consulta y protocolo de secuencia --------------------------------

    def __len__(self):                           # len(l)
        return self.tamano

    def vacia(self):
        return self.tamano == 0

    def __iter__(self):                          # for x in l
        # Un GENERADOR: cada "yield" entrega un dato y el bucle se queda
        # parado ahi hasta que el for pide el siguiente.
        actual = self.cabeza
        while actual is not None:
            yield actual.dato
            actual = actual.siguiente

    def __reversed__(self):                      # reversed(l)
        actual = self.cola
        while actual is not None:
            yield actual.dato
            actual = actual.anterior

    def buscar(self, dato):
        # Coste de cada paso: O(?)   Recorrido completo: O(?)
        # TODO: igual que __iter__ pero empezando por la cola y yendo hacia atras.
        raise NotImplementedError

    def __str__(self):
        return "[" + " <-> ".join(repr(d) for d in self) + "]"

    def print_forward(self):
        print(" <-> ".join(str(d) for d in self))

    def print_backward(self):
        print(" <-> ".join(str(d) for d in reversed(self)))

    # --- Insercion (todos devuelven el nodo nuevo) ---------------------------

    def insert_first(self, dato):
        # O(1). Hecho como ejemplo: los 4 punteros de la diapositiva.
        nuevo = NodoDoble(dato)
        if self.cabeza is None:              # lista vacia: EL caso especial
            self.cabeza = self.cola = nuevo
        else:
            nuevo.siguiente = self.cabeza    # 1. X.siguiente = cabeza
            # 2. X.anterior = None (ya lo es al crear el nodo)
            self.cabeza.anterior = nuevo     # 3. cabeza.anterior = X
            self.cabeza = nuevo              # 4. cabeza = X
        self.tamano += 1
        return nuevo

    def insert_last(self, dato):
        # Coste: O(?)
        # TODO: simetrico a insert_first, trabajando sobre la cola.
        raise NotImplementedError

    def insert_before(self, nodo, dato):
        # Coste: O(?)
        # pre: nodo es un nodo de ESTA lista.
        # TODO: caso especial -> nodo es la cabeza (usa insert_first).
        raise NotImplementedError

    def insert_after(self, nodo, dato):
        # Coste: O(?)
        # pre: nodo es un nodo de ESTA lista.
        # TODO: caso especial -> nodo es la cola (usa insert_last).
        raise NotImplementedError

    # --- Borrado ------------------------------------------------------------

    def delete_node(self, nodo):
        # Coste: O(?)
        # pre : nodo es un nodo de ESTA lista.
        # post: devuelve nodo.dato y deja nodo.anterior y nodo.siguiente a None.
        # TODO: reconectar el enlace izquierdo (o mover cabeza si nodo era la cabeza)
        # TODO: reconectar el enlace derecho (o mover cola si nodo era la cola)
        # TODO: actualizar tamano
        raise NotImplementedError

    def delete_first(self):
        # Coste: O(?)
        # Si la lista esta vacia: raise IndexError("..."), como list.pop().
        # Devuelve el dato borrado. Pista: es un caso particular de delete_node.
        raise NotImplementedError

    def delete_last(self):
        # Coste: O(?)
        # Si la lista esta vacia: raise IndexError("..."), como list.pop().
        raise NotImplementedError

    # --- Palindromo ---------------------------------------------------------

    def es_palindromo(self):
        # Coste: O(?) en tiempo y O(?) en memoria auxiliar.
        # TODO: dos punteros, inicio = self.cabeza y fin = self.cola, que
        #       avanzan hacia el centro. Bastan tamano // 2 comparaciones.
        raise NotImplementedError

    # --- Ampliacion (opcional, no puntua) -------------------------------------

    def reverse(self):
        # Coste: O(?). Sin crear nodos nuevos.
        #   [1, 2, 3] -> [3, 2, 1]
        # TODO: en cada nodo, intercambia .anterior y .siguiente
        #       (a, b = b, a); al final, intercambia cabeza y cola.
        raise NotImplementedError

    def intercalar(self, otra):
        # Coste: O(?). otra NO se modifica.
        #   [1, 3, 5].intercalar([2, 4, 6, 8, 10]) -> [1, 2, 3, 4, 5, 6, 8, 10]
        # TODO: usa insert_after sobre el nodo actual de self y, cuando self
        #       se acabe, insert_last.
        raise NotImplementedError

    def rotar(self, k, derecha=True):
        # Coste: O(?). Sin crear nodos nuevos.
        #   [1,2,3,4,5].rotar(2)                -> [4,5,1,2,3]
        #   [1,2,3,4,5].rotar(2, derecha=False) -> [3,4,5,1,2]
        # TODO: normaliza k %= tamano, localiza la nueva cola y reconecta.
        raise NotImplementedError

    # --- Comprobacion explicita del invariante (no se toca) --------------

    def invariante_correcto(self):
        if self.tamano < 0:
            return False
        if self.tamano == 0:
            return self.cabeza is None and self.cola is None
        if self.cabeza is None or self.cola is None:
            return False
        if self.cabeza.anterior is not None or self.cola.siguiente is not None:
            return False
        contados = 0
        previo = None
        actual = self.cabeza
        while actual is not None:
            contados += 1
            if contados > self.tamano:          # evita colgarse con un ciclo
                return False
            if actual.anterior is not previo:   # el enlace hacia atras cuadra
                return False
            previo = actual
            actual = actual.siguiente
        return contados == self.tamano and previo is self.cola


def main_lista():
    # Entrada/salida del juez (DOMjudge, problema "Lista doble"). Ya esta
    # hecho: no lo toques. Una orden por linea; los datos son palabras.
    #   insert_first X | insert_last X       insertar X al principio / al final
    #   insert_before A X | insert_after A X  insertar X antes / despues del primer A
    #   delete_first | delete_last | delete A borrar (escribe el dato borrado)
    #   palindromo | size | print | print_back
    # Si no se puede borrar o no existe A, se escribe ERROR. Lista vacia: "-".
    import sys
    l = ListaDoble()
    salida = []
    for linea in sys.stdin.read().split("\n"):
        partes = linea.split()
        if not partes:
            continue
        orden, args = partes[0], partes[1:]
        if orden == "insert_first":
            l.insert_first(args[0])
        elif orden == "insert_last":
            l.insert_last(args[0])
        elif orden in ("insert_before", "insert_after"):
            nodo = l.buscar(args[0])
            if nodo is None:
                salida.append("ERROR")
            else:
                getattr(l, orden)(nodo, args[1])
        elif orden in ("delete_first", "delete_last"):
            try:
                salida.append(getattr(l, orden)())
            except IndexError:
                salida.append("ERROR")
        elif orden == "delete":
            nodo = l.buscar(args[0])
            salida.append("ERROR" if nodo is None else l.delete_node(nodo))
        elif orden == "palindromo":
            salida.append("SI" if l.es_palindromo() else "NO")
        elif orden == "size":
            salida.append(str(len(l)))
        elif orden == "print":
            salida.append(" ".join(l) if len(l) else "-")
        elif orden == "print_back":
            salida.append(" ".join(reversed(l)) if len(l) else "-")
    if salida:
        print("\n".join(salida))


if __name__ == "__main__":
    # Probar como lo hara el juez:  python3 lista_doble.py < ejemplo_lista.txt
    main_lista()
