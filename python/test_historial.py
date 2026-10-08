# test_historial.py
# Pruebas del Historial de Navegador (trabajo de casa). No hay que
# modificarlo: hay que conseguir que pase entero.
#
#   python3 -m unittest -v test_historial
#
# Necesita que la ListaDoble ya pase sus pruebas (test_lista_doble).

import gc
import unittest

from historial import BrowserHistory
from lista_doble import NodoDoble


class PruebaBase(unittest.TestCase):
    def comprobar(self, bh, paginas, actual, despues_de=""):
        # Comprueba la ListaDoble interna completa y donde esta 'actual'.
        self.assertTrue(bh.paginas.invariante_correcto(),
                        f"invariante de la lista roto tras {despues_de}")
        self.assertEqual(list(bh.paginas), paginas, f"paginas tras {despues_de}")
        self.assertEqual(bh.actual.dato, actual, f"pagina actual tras {despues_de}")


class PruebasHistorial(PruebaBase):
    def test_pagina_de_inicio(self):
        bh = BrowserHistory("leetcode.com")
        self.comprobar(bh, ["leetcode.com"], "leetcode.com", "crear")
        self.assertEqual(bh.back(1), "leetcode.com")
        self.assertEqual(bh.forward(1), "leetcode.com")

    def test_visit_avanza(self):
        bh = BrowserHistory("a")
        bh.visit("b")
        bh.visit("c")
        self.comprobar(bh, ["a", "b", "c"], "c", "dos visit")

    def test_back_y_forward(self):
        bh = BrowserHistory("a")
        for url in "bcd":
            bh.visit(url)
        self.assertEqual(bh.back(1), "c")
        self.assertEqual(bh.back(2), "a")
        self.assertEqual(bh.forward(2), "c")
        self.comprobar(bh, ["a", "b", "c", "d"], "c", "back/forward (no borran nada)")

    def test_topes(self):
        bh = BrowserHistory("a")
        bh.visit("b")
        self.assertEqual(bh.back(100), "a")      # no revienta aunque pidas de mas
        self.assertEqual(bh.forward(100), "b")
        self.assertEqual(bh.back(0), "b")

    def test_visit_descarta_lo_de_delante(self):
        bh = BrowserHistory("leetcode.com")
        for url in ("google.com", "facebook.com", "youtube.com"):
            bh.visit(url)
        bh.back(1)
        bh.visit("linkedin.com")
        self.comprobar(bh, ["leetcode.com", "google.com", "facebook.com", "linkedin.com"],
                       "linkedin.com", "visit tras back")
        self.assertEqual(bh.forward(1), "linkedin.com")

    def test_visit_desde_el_principio(self):
        bh = BrowserHistory("a")
        for url in "bcde":
            bh.visit(url)
        bh.back(10)
        bh.visit("x")
        self.comprobar(bh, ["a", "x"], "x", "visit desde la primera pagina")

    def test_traza_del_enunciado(self):
        bh = BrowserHistory("leetcode.com")
        bh.visit("google.com")
        bh.visit("facebook.com")
        bh.visit("youtube.com")
        self.assertEqual(bh.back(1), "facebook.com")
        self.assertEqual(bh.back(1), "google.com")
        self.assertEqual(bh.forward(1), "facebook.com")
        bh.visit("linkedin.com")                     # descarta youtube.com
        self.assertEqual(bh.forward(2), "linkedin.com")
        self.assertEqual(bh.back(2), "google.com")
        self.assertEqual(bh.back(7), "leetcode.com")


class PruebaContraList(PruebaBase):
    # Oraculo: un historial hecho con una list y un indice, que sabemos que
    # es correcto (y que es como lo haria cualquiera sin listas enlazadas).
    def test_navegacion_aleatoria(self):
        import random
        rng = random.Random(1472)
        bh = BrowserHistory("p0")
        modelo, pos = ["p0"], 0
        for paso in range(3000):
            op = rng.choice(["visit", "back", "forward"])
            if op == "visit":
                url = f"p{paso}"
                bh.visit(url)
                del modelo[pos + 1:]
                modelo.append(url)
                pos += 1
            else:
                k = rng.randint(0, 6)
                if op == "back":
                    pos = max(0, pos - k)
                    self.assertEqual(bh.back(k), modelo[pos], f"paso {paso}")
                else:
                    pos = min(len(modelo) - 1, pos + k)
                    self.assertEqual(bh.forward(k), modelo[pos], f"paso {paso}")
            self.comprobar(bh, modelo, modelo[pos], f"paso {paso} ({op})")


class PruebasMemoria(PruebaBase):
    # Ejercicio 4: las paginas descartadas por visit() deben quedar libres en
    # cuanto se descartan, sin depender del recolector de ciclos.
    def setUp(self):
        gc.collect()
        gc.disable()

    def tearDown(self):
        gc.enable()

    def test_visit_libera_las_paginas_descartadas(self):
        bh = BrowserHistory("inicio")
        for i in range(100):
            bh.visit(f"p{i}")
        bh.back(100)
        antes = NodoDoble.vivos
        bh.visit("nueva")                # descarta 100 paginas, crea 1
        self.comprobar(bh, ["inicio", "nueva"], "nueva", "visit que descarta 100 paginas")
        self.assertEqual(NodoDoble.vivos, antes - 100 + 1,
                         "las paginas descartadas siguen vivas: forman un ciclo "
                         "de referencias (rompe sus enlaces al descartarlas)")


if __name__ == "__main__":
    unittest.main(verbosity=2)
