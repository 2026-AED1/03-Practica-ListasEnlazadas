# historial.py
# Practica 3 - Historial de navegador con atras/adelante (LeetCode #1472),
# construido sobre TU ListaDoble. Parte 3: se explica en clase y se programa en CASA.
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
        # Coste: O(1) amortizado
        while self.paginas.cola is not self.actual:
            self.paginas.delete_last()
        self.actual = self.paginas.insert_after(self.actual, url)

    def back(self, steps):
        # Coste: O(min(steps, n))
        while steps > 0 and self.actual.anterior is not None:
            self.actual = self.actual.anterior
            steps -= 1
        return self.actual.dato

    def forward(self, steps):
        # Coste: O(min(steps, n))
        while steps > 0 and self.actual.siguiente is not None:
            self.actual = self.actual.siguiente
            steps -= 1
        return self.actual.dato

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
