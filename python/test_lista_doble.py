# test_lista_doble.py
# Pruebas de autocomprobacion de la ListaDoble. No hay que modificarlo: hay
# que conseguir que pase entero.
#
# Todas las pruebas comprueban, ademas del resultado, el INVARIANTE de la
# representacion despues de cada operacion (y el recorrido hacia atras en
# cuanto __reversed__ esta hecho; mientras no, solo falla test_reversed). Un fallo "invariante roto tras
# ..." significa que el resultado puede parecer correcto pero la estructura
# interna ha quedado inconsistente (tipico: un .anterior que no se actualizo,
# o cola apuntando a un nodo que ya no esta en la lista).
#
# Se ejecuta por grupos, en el mismo orden en que se programa en clase:
#   python3 -m unittest -v test_lista_doble.PruebasInsercion
#   python3 -m unittest -v test_lista_doble.PruebasInsercionRelativa
#   python3 -m unittest -v test_lista_doble.PruebasBorrado
#   python3 -m unittest -v test_lista_doble.PruebaContraList
#   python3 -m unittest -v test_lista_doble.PruebasPalindromo
# Ampliacion (opcional; se saltan mientras no esten hechos):
#   PruebasReverse, PruebasIntercalar, PruebasRotar
# Todo:
#   python3 -m unittest -v test_lista_doble

import random
import unittest

from lista_doble import ListaDoble, NodoDoble


class PruebaBase(unittest.TestCase):
    def opcional(self, funcion, *args):
        # Ejecuta un metodo de la ampliacion; si no esta hecho, salta la prueba.
        try:
            return funcion(*args)
        except NotImplementedError:
            self.skipTest("ampliacion opcional sin implementar")

    def comprobar(self, lista, esperado, despues_de=""):
        self.assertTrue(lista.invariante_correcto(),
                        f"invariante roto tras {despues_de}")
        self.assertEqual(len(lista), len(esperado), f"tamano tras {despues_de}")
        self.assertEqual(list(lista), esperado, f"recorrido hacia delante tras {despues_de}")
        try:
            hacia_atras = list(reversed(lista))
        except NotImplementedError:
            # __reversed__ sigue en TODO (paso 1): de momento no se comprueba
            # aqui; lo comprueba test_reversed. El invariante ya revisa .anterior.
            return
        self.assertEqual(hacia_atras, esperado[::-1],
                         f"recorrido hacia atras tras {despues_de}")


class PruebasInsercion(PruebaBase):
    def test_lista_nueva_vacia(self):
        l = ListaDoble()
        self.assertTrue(l.vacia())
        self.comprobar(l, [], "crear")

    def test_insert_last(self):
        l = ListaDoble()
        for v in [10, 20, 30]:
            l.insert_last(v)
        self.comprobar(l, [10, 20, 30], "insert_last")
        self.assertEqual(l.cola.anterior.dato, 20)

    def test_reversed(self):
        # reversed(l) llama a __reversed__ (TODO del paso 1).
        self.assertEqual(list(reversed(ListaDoble())), [])
        l = ListaDoble()
        for v in [1, 2, 3]:
            l.insert_first(v)                    # ya hecho: [3, 2, 1]
        self.assertEqual(list(reversed(l)), [1, 2, 3])

    def test_insert_first(self):
        l = ListaDoble()
        for v in [1, 2, 3]:
            l.insert_first(v)
        self.comprobar(l, [3, 2, 1], "insert_first")

    def test_primera_insercion_actualiza_cabeza_y_cola(self):
        # EL bug mas comun de la practica: la lista vacia.
        for metodo in ("insert_first", "insert_last"):
            with self.subTest(metodo=metodo):
                l = ListaDoble()
                getattr(l, metodo)(7)
                self.assertIs(l.cabeza, l.cola)
                self.comprobar(l, [7], metodo + " en lista vacia")

    def test_mezcla_principio_y_final(self):
        l = ListaDoble()
        l.insert_last(10)
        l.insert_last(20)
        l.insert_first(5)
        self.comprobar(l, [5, 10, 20], "mezclar inserciones")
        self.assertEqual(l.cabeza.dato, 5)
        self.assertEqual(l.cola.dato, 20)

    def test_insert_devuelve_el_nodo(self):
        l = ListaDoble()
        nodo = l.insert_last("a")
        self.assertIsInstance(nodo, NodoDoble)
        self.assertIs(nodo, l.cola)
        self.assertIs(l.insert_first("b"), l.cabeza)

    def test_constructor_con_iterable(self):
        self.comprobar(ListaDoble(range(5)), [0, 1, 2, 3, 4], "ListaDoble(range(5))")

    def test_protocolo_de_secuencia(self):
        # Todo esto funciona "gratis" en cuanto existen __len__ e __iter__.
        l = ListaDoble([3, 1, 2])
        self.assertIn(1, l)
        self.assertNotIn(9, l)
        self.assertEqual(sum(l), 6)
        self.assertEqual(sorted(l), [1, 2, 3])
        self.assertEqual(list(reversed(l)), [2, 1, 3])
        self.assertEqual(str(l), "[3 <-> 1 <-> 2]")


class PruebasBorrado(PruebaBase):
    def test_delete_first(self):
        l = ListaDoble([1, 2, 3])
        self.assertEqual(l.delete_first(), 1)
        self.comprobar(l, [2, 3], "delete_first")

    def test_delete_last(self):
        l = ListaDoble([1, 2, 3])
        self.assertEqual(l.delete_last(), 3)
        self.comprobar(l, [1, 2], "delete_last")

    def test_delete_node_en_medio(self):
        l = ListaDoble(["A", "B", "C"])
        self.assertEqual(l.delete_node(l.buscar("B")), "B")
        self.comprobar(l, ["A", "C"], "delete_node en medio")

    def test_delete_node_extremos(self):
        l = ListaDoble(["A", "B", "C"])
        l.delete_node(l.cabeza)
        self.comprobar(l, ["B", "C"], "delete_node(cabeza)")
        l.delete_node(l.cola)
        self.comprobar(l, ["B"], "delete_node(cola)")
        l.delete_node(l.cabeza)
        self.comprobar(l, [], "delete_node del unico elemento")

    def test_vaciar_y_reutilizar(self):
        # Si al borrar el unico elemento cabeza o cola siguen apuntando al
        # nodo borrado, la siguiente insercion lo engancha ahi.
        for borrar in ("delete_first", "delete_last"):
            for insertar in ("insert_first", "insert_last"):
                with self.subTest(borrar=borrar, insertar=insertar):
                    l = ListaDoble([7])
                    getattr(l, borrar)()
                    self.comprobar(l, [], borrar + " del unico elemento")
                    getattr(l, insertar)(8)
                    self.comprobar(l, [8], insertar + " tras vaciar")

    def test_borrar_en_vacia_lanza_indexerror(self):
        # Igual que list.pop() sobre una lista vacia.
        l = ListaDoble()
        with self.assertRaises(IndexError):
            l.delete_first()
        with self.assertRaises(IndexError):
            l.delete_last()


class PruebasInsercionRelativa(PruebaBase):
    def test_insert_before(self):
        l = ListaDoble(["A", "C"])
        nuevo = l.insert_before(l.buscar("C"), "B")
        self.assertEqual(nuevo.dato, "B")
        self.comprobar(l, ["A", "B", "C"], "insert_before en medio")
        l.insert_before(l.cabeza, "inicio")
        self.comprobar(l, ["inicio", "A", "B", "C"], "insert_before(cabeza)")

    def test_insert_after(self):
        l = ListaDoble(["A", "C"])
        nuevo = l.insert_after(l.buscar("A"), "B")
        self.assertEqual(nuevo.dato, "B")
        self.comprobar(l, ["A", "B", "C"], "insert_after en medio")
        l.insert_after(l.cola, "fin")
        self.comprobar(l, ["A", "B", "C", "fin"], "insert_after(cola)")

    def test_insertar_alrededor_de_un_unico_nodo(self):
        l = ListaDoble([5])
        l.insert_before(l.cabeza, 4)
        l.insert_after(l.cola, 6)
        self.comprobar(l, [4, 5, 6], "insert_before/after con un solo nodo")


class PruebasReverse(PruebaBase):
    # Ampliacion opcional: si reverse no esta hecho, estas pruebas se saltan.
    def test_reverse(self):
        for valores in ([], [1], [1, 2], [1, 2, 3, 4, 5]):
            with self.subTest(valores=valores):
                l = ListaDoble(valores)
                self.opcional(l.reverse)
                self.comprobar(l, valores[::-1], f"reverse de {valores}")

    def test_reverse_no_crea_nodos(self):
        l = ListaDoble([1, 2, 3])
        nodos = [l.cabeza, l.cabeza.siguiente, l.cola]
        self.opcional(l.reverse)
        self.assertIs(l.cabeza, nodos[2])
        self.assertIs(l.cabeza.siguiente, nodos[1])
        self.assertIs(l.cola, nodos[0])

    def test_reverse_y_despues_insertar(self):
        l = ListaDoble([1, 2, 3])
        self.opcional(l.reverse)
        l.insert_last(0)
        l.insert_first(4)
        self.comprobar(l, [4, 3, 2, 1, 0], "insertar tras reverse")


class PruebasPalindromo(PruebaBase):
    def test_palindromos(self):
        for valores in ([], [1], [1, 1], [1, 2, 1], [1, 2, 2, 1], [1, 2, 3, 2, 1],
                        list("reconocer")):
            with self.subTest(valores=valores):
                l = ListaDoble(valores)
                self.assertTrue(l.es_palindromo())
                self.comprobar(l, valores, "es_palindromo (no debe modificar la lista)")

    def test_no_palindromos(self):
        for valores in ([1, 2], [1, 2, 3], [1, 2, 3, 4, 5], [1, 2, 3, 1],
                        list("palindromo")):
            with self.subTest(valores=valores):
                self.assertFalse(ListaDoble(valores).es_palindromo())


class PruebaContraList(PruebaBase):
    # La list de Python como ORACULO: se hacen las mismas operaciones
    # aleatorias sobre las dos estructuras y tienen que coincidir siempre.
    def test_operaciones_aleatorias(self):
        rng = random.Random(2026)
        l = ListaDoble()
        modelo = []
        for paso in range(2000):
            op = rng.choice(["ini", "fin", "bpri", "bult", "antes", "despues",
                             "nodo", "rev"])
            v = rng.randint(0, 99)
            if op == "ini":
                l.insert_first(v)
                modelo.insert(0, v)
            elif op == "fin":
                l.insert_last(v)
                modelo.append(v)
            elif op == "bpri" and modelo:
                self.assertEqual(l.delete_first(), modelo.pop(0))
            elif op == "bult" and modelo:
                self.assertEqual(l.delete_last(), modelo.pop())
            elif op in ("antes", "despues", "nodo") and modelo:
                i = rng.randrange(len(modelo))
                nodo = l.cabeza
                for _ in range(i):
                    nodo = nodo.siguiente
                if op == "antes":
                    l.insert_before(nodo, v)
                    modelo.insert(i, v)
                elif op == "despues":
                    l.insert_after(nodo, v)
                    modelo.insert(i + 1, v)
                else:
                    self.assertEqual(l.delete_node(nodo), modelo.pop(i))
            elif op == "rev" and rng.random() < 0.2:
                try:                        # reverse se hace en casa: si aun
                    l.reverse()             # no esta, esta operacion se salta
                    modelo.reverse()
                except NotImplementedError:
                    pass
            self.comprobar(l, modelo, f"paso {paso} ({op})")
        self.assertEqual(l.es_palindromo(), modelo == modelo[::-1])


class PruebasIntercalar(PruebaBase):
    # Ampliacion opcional: si intercalar no esta hecho, estas pruebas se saltan.
    def caso(self, a, b, esperado):
        la, lb = ListaDoble(a), ListaDoble(b)
        self.opcional(la.intercalar, lb)
        self.comprobar(la, esperado, f"intercalar({a}, {b})")
        self.comprobar(lb, b, "intercalar (la otra lista no debe cambiar)")
        la.insert_last("x")                 # destapa una cola mal actualizada
        self.comprobar(la, esperado + ["x"], "insert_last tras intercalar")

    def test_misma_longitud(self):
        self.caso([1, 3, 5], [2, 4, 6], [1, 2, 3, 4, 5, 6])

    def test_otra_mas_larga(self):
        self.caso([1, 3], [2, 4, 6, 8], [1, 2, 3, 4, 6, 8])

    def test_otra_mas_corta(self):
        self.caso([1, 3, 5, 7], [2], [1, 2, 3, 5, 7])

    def test_listas_vacias(self):
        self.caso([], [1, 2], [1, 2])
        self.caso([1, 2], [], [1, 2])
        self.caso([], [], [])


class PruebasRotar(PruebaBase):
    # Ampliacion opcional: si rotar no esta hecho, estas pruebas se saltan.
    def rotar(self, valores, k, derecha=True):
        l = ListaDoble(valores)
        self.opcional(l.rotar, k, derecha)
        return l

    def test_rotar_derecha(self):
        for k, esperado in [(0, [1, 2, 3, 4, 5]), (2, [4, 5, 1, 2, 3]),
                            (5, [1, 2, 3, 4, 5]), (7, [4, 5, 1, 2, 3])]:
            with self.subTest(k=k):
                self.comprobar(self.rotar([1, 2, 3, 4, 5], k), esperado, f"rotar({k})")

    def test_rotar_izquierda(self):
        self.comprobar(self.rotar([1, 2, 3, 4, 5], 2, derecha=False),
                       [3, 4, 5, 1, 2], "rotar(2, derecha=False)")

    def test_rotar_no_crea_nodos(self):
        l = ListaDoble([1, 2, 3, 4])
        nodos = {id(l.cabeza), id(l.cabeza.siguiente), id(l.cola.anterior), id(l.cola)}
        self.opcional(l.rotar, 1)
        self.comprobar(l, [4, 1, 2, 3], "rotar(1)")
        nodo, despues = l.cabeza, set()
        while nodo is not None:
            despues.add(id(nodo))
            nodo = nodo.siguiente
        self.assertEqual(despues, nodos, "rotar debe reutilizar los mismos nodos")

    def test_rotar_casos_pequenos(self):
        self.comprobar(self.rotar([], 3), [], "rotar lista vacia")
        self.comprobar(self.rotar([1], 3), [1], "rotar lista de 1")


if __name__ == "__main__":
    unittest.main(verbosity=2)
