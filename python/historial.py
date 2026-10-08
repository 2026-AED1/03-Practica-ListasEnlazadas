# historial.py
# Practica 3 - Historial de navegador con atras/adelante (LeetCode #1472),
# construido sobre TU ListaDoble. Trabajo de CASA (Ejercicio 3).
#
# No hace falta ninguna estructura nueva (ni diccionario ni tabla hash): las
# paginas van en una ListaDoble y un unico puntero, 'actual', dice en que
# NODO estamos.
#
#   paginas:  leetcode.com <-> google.com <-> facebook.com <-> youtube.com
#                                                 ^
#                                               actual
#
# Ejecutar los tests (cuando test_lista_doble ya pase):
#   python3 -m unittest -v test_historial
#
# Probar como lo hara el juez (lee ordenes de la entrada estandar):
#   python3 historial.py < ejemplo_historial.txt
# Al juez (problema "Historial de navegador") se sube UN fichero que lleva
# tambien tu ListaDoble: generalo con  python3 generar_envio.py  y sube
# envio_historial.py.

import sys

from lista_doble import ListaDoble


class BrowserHistory:
    # Invariante: actual es un nodo de self.paginas (nunca None).

    def __init__(self, homepage):
        self.paginas = ListaDoble()
        self.actual = self.paginas.insert_last(homepage)

    def visit(self, url):
        # Coste: O(?)   (pista: "amortizado")
        # TODO:
        # 1. Descartar todas las paginas que hay POR DELANTE de self.actual.
        #    Tienen que quedar desenganchadas de verdad (Ejercicio 4): si solo
        #    cortas el enlace actual.siguiente, las paginas descartadas siguen
        #    apuntandose entre si y forman un ciclo. Pista: tu ListaDoble ya
        #    sabe borrar por el final dejando los punteros a None.
        # 2. Enlazar un nodo nuevo con url justo detras de self.actual.
        # 3. Mover self.actual a ese nodo nuevo.
        raise NotImplementedError

    def back(self, steps):
        # Coste: O(?)
        # TODO: mientras queden steps y exista self.actual.anterior,
        #       retrocede self.actual. Devuelve self.actual.dato.
        raise NotImplementedError

    def forward(self, steps):
        # Coste: O(?)
        # TODO: mientras queden steps y exista self.actual.siguiente,
        #       avanza self.actual. Devuelve self.actual.dato.
        raise NotImplementedError

    def __str__(self):
        partes = []
        nodo = self.paginas.cabeza
        while nodo is not None:
            partes.append(f"[{nodo.dato}]" if nodo is self.actual else nodo.dato)
            nodo = nodo.siguiente
        return " <-> ".join(partes)


def main():
    # Entrada/salida del juez (DOMjudge). Ya esta hecho: no lo toques.
    # Primera linea: la pagina de inicio. Despues, una orden por linea:
    #   visit URL  |  back K  |  forward K
    # Por cada back o forward se escribe la pagina en la que se queda.
    lineas = sys.stdin.read().split("\n")
    bh = BrowserHistory(lineas[0].strip())
    salida = []
    for linea in lineas[1:]:
        partes = linea.split()
        if not partes:
            continue
        orden, arg = partes[0], partes[1]
        if orden == "visit":
            bh.visit(arg)
        elif orden == "back":
            salida.append(bh.back(int(arg)))
        elif orden == "forward":
            salida.append(bh.forward(int(arg)))
    if salida:
        print("\n".join(salida))


if __name__ == "__main__":
    main()
