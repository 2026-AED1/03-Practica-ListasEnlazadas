# comparativa.py  --  AMPLIACION OPCIONAL (no puntua)
# Objetivo: comprobar con el reloj lo que dice la teoria: un segundo puntero
# (anterior) convierte en O(1) operaciones que en la lista simple son O(n)...
# y averiguar cuanto cuesta ese puntero en memoria.
#
# No hay que programar nada aqui. Antes de cada experimento, apunta en
# RESPUESTAS.md lo que esperas; despues ejecutalo y compara.
#
# Metodo: no nos interesa el tiempo absoluto (depende del ordenador), sino
# como CRECE. Cada tabla mide con n, 2n, 4n, 8n y muestra la razon t(2n)/t(n):
#    razon ~ 1  -> O(1) (no depende de n)
#    razon ~ 2  -> O(n)
#    razon ~ 4  -> O(n^2)
#
# Experimentos:
#   A) vaciar una lista borrando siempre el ULTIMO
#   B) borrar nodos de los que ya tenemos la referencia
#   C) recorrer hacia atras
#   D) memoria por elemento: el precio del puntero 'anterior'
#
# Ejecutar todos (menos de un minuto), o solo algunos:
#   python3 comparativa.py
#   python3 comparativa.py A D

import collections
import random
import sys
import time
import tracemalloc

from lista_doble import ListaDoble
from lista_simple import ListaSimple


# =====================================================================
# Herramientas de medida
# =====================================================================

def cronometrar(funcion, repeticiones=3, tiempo_minimo=0.2):
    # El MINIMO de varias repeticiones es la medida mas estable: el ruido
    # (otros procesos, el recolector de basura) solo puede sumar tiempo.
    mejor = float("inf")
    total = 0.0
    veces = 0
    while veces < repeticiones or (total < tiempo_minimo and veces < 500):
        t0 = time.perf_counter()
        funcion()
        t = time.perf_counter() - t0
        mejor = min(mejor, t)
        total += t
        veces += 1
    return mejor


def tabla(titulo, tamanios, columnas, repeticiones=3, tiempo_minimo=0.2):
    # columnas: lista de (nombre, preparar). preparar(n) construye lo que
    # haga falta (sin cronometrar) y devuelve la funcion que SI se mide.
    print()
    print(titulo)
    print("-" * len(titulo))
    cabecera = f"{'n':>8}"
    for nombre, _ in columnas:
        cabecera += f" | {nombre:>24}"
    print(cabecera)
    anteriores = [None] * len(columnas)
    for n in tamanios:
        fila = f"{n:>8}"
        for i, (_, preparar) in enumerate(columnas):
            try:
                t = cronometrar(preparar(n), repeticiones, tiempo_minimo)
            except NotImplementedError:
                fila += f" | {'(pendiente)':>24}"
                continue
            razon = ""
            if anteriores[i]:
                razon = f"x{t / anteriores[i]:.1f}"
            anteriores[i] = t
            fila += f" | {t * 1000:>12.3f} ms {razon:>8}"
        print(fila)


# =====================================================================
# A) Vaciar borrando siempre el ultimo
# =====================================================================

def experimento_a():
    def vaciar_por_el_final(construir, borrar):
        def preparar(n):
            def f():
                estructura = construir(range(n))   # (se mide tambien, es O(n))
                for _ in range(n):
                    borrar(estructura)
            return f
        return preparar

    tabla("A) Construir una lista de n elementos y vaciarla borrando el ULTIMO",
          [1_000, 2_000, 4_000, 8_000],
          [("ListaSimple.delete_last", vaciar_por_el_final(ListaSimple, ListaSimple.delete_last)),
           ("ListaDoble.delete_last", vaciar_por_el_final(ListaDoble, ListaDoble.delete_last)),
           ("list.pop()", vaciar_por_el_final(list, list.pop))],
          repeticiones=1)


# =====================================================================
# B) Borrar nodos de los que ya tenemos la referencia
# =====================================================================

def experimento_b():
    m = 2000                                # borrados por medida

    def borrar_nodos(construir):
        def preparar(n):
            estructura = construir(range(n))
            # Guardamos referencias a m nodos al azar ANTES de medir (como
            # hace el historial con 'actual': ya sabemos donde esta el nodo).
            nodos = []
            nodo = estructura.cabeza
            elegidos = set(random.sample(range(n), m))
            for i in range(n):
                if i in elegidos:
                    nodos.append(nodo)
                nodo = nodo.siguiente
            random.shuffle(nodos)

            def f():
                for nodo in nodos:
                    estructura.delete_node(nodo)
            return f
        return preparar

    def list_remove(n):
        l = list(range(n))
        valores = random.sample(range(n), m)

        def f():
            for v in valores:
                l.remove(v)                 # busca el valor y desplaza el resto
        return f

    tabla(f"B) Borrar {m} nodos de los que YA tenemos la referencia",
          [10_000, 20_000, 40_000, 80_000],
          [("ListaSimple.delete_node", borrar_nodos(ListaSimple)),
           ("ListaDoble.delete_node", borrar_nodos(ListaDoble)),
           ("list.remove(x)", list_remove)],
          repeticiones=1, tiempo_minimo=0)


# =====================================================================
# C) Recorrer hacia atras
# =====================================================================

def experimento_c():
    def atras_con_reversed(construir):
        def preparar(n):
            estructura = construir(range(n))

            def f():
                total = 0
                for x in reversed(estructura):
                    total += x
            return f
        return preparar

    def atras_con_indices(n):
        # La lista simple no sabe ir hacia atras: la unica forma es pedir
        # l[n-1], l[n-2], ... y cada l[i] empieza otra vez desde la cabeza.
        estructura = ListaSimple(range(n))

        def f():
            total = 0
            for i in range(len(estructura) - 1, -1, -1):
                total += estructura[i]
        return f

    tabla("C) Sumar todos los elementos recorriendo de la cola a la cabeza",
          [1_000, 2_000, 4_000, 8_000],
          [("ListaSimple, l[i]", atras_con_indices),
           ("reversed(ListaDoble)", atras_con_reversed(ListaDoble)),
           ("reversed(list)", atras_con_reversed(list))],
          repeticiones=1)


# =====================================================================
# D) Memoria por elemento
# =====================================================================

def experimento_d():
    n = 100_000
    # Los valores se crean ANTES de medir: solo se cuenta el contenedor.
    valores = list(range(1000, 1000 + n))

    def con_append(vs):
        l = []
        for v in vs:
            l.append(v)
        return l

    def bytes_por_elemento(construir):
        tracemalloc.start()
        antes = tracemalloc.get_traced_memory()[0]
        estructura = construir(valores)
        despues = tracemalloc.get_traced_memory()[0]
        tracemalloc.stop()
        del estructura
        return (despues - antes) / n

    titulo = f"D) Memoria del contenedor, en bytes por elemento (n = {n})"
    print()
    print(titulo)
    print("-" * len(titulo))
    for nombre, construir in [("list (con append)", con_append),
                              ("collections.deque", collections.deque),
                              ("ListaSimple", ListaSimple),
                              ("ListaDoble", ListaDoble)]:
        try:
            print(f"  {nombre:<22} {bytes_por_elemento(construir):>7.1f} B")
        except NotImplementedError:
            tracemalloc.stop()
            print(f"  {nombre:<22} (pendiente)")


# =====================================================================

EXPERIMENTOS = {
    "A": experimento_a, "B": experimento_b, "C": experimento_c,
    "D": experimento_d,
}

if __name__ == "__main__":
    random.seed(2026)
    elegidos = [a.upper() for a in sys.argv[1:]] or list(EXPERIMENTOS)
    for letra in elegidos:
        if letra not in EXPERIMENTOS:
            print(f"Experimento desconocido: {letra} (validos: A-D)")
            continue
        try:
            EXPERIMENTOS[letra]()
        except NotImplementedError:
            print("  (pendiente: este experimento necesita metodos que aun no has hecho)")
    print()
