// test_historial.cpp
// Pruebas del Historial de Navegador en C++ (trabajo de casa). No hay que modificarlo.
//
// Compilar (desde la carpeta cpp/):
//   g++ -std=c++17 -Wall test_historial.cpp -o test_historial
//   ./test_historial

#include <random>
#include <string>
#include <vector>

#include "historial.hpp"
#include "mini_test.hpp"

using Nodo = ListaDoble<std::string>::Nodo;

static void comprobar(const BrowserHistory& bh, const std::vector<std::string>& paginas,
                      const std::string& actual, const std::string& tras) {
    COMPROBAR(bh.paginas.invariante_correcto(), "invariante de la lista roto tras " + tras);
    COMPROBAR(bh.paginas.to_vector() == paginas, "paginas tras " + tras);
    COMPROBAR(bh.actual != nullptr && bh.actual->dato == actual, "pagina actual tras " + tras);
}

PRUEBA(PruebasHistorial, pagina_de_inicio) {
    BrowserHistory bh("leetcode.com");
    comprobar(bh, {"leetcode.com"}, "leetcode.com", "crear");
    COMPROBAR(bh.back(1) == "leetcode.com", "back sin historial");
    COMPROBAR(bh.forward(1) == "leetcode.com", "forward sin historial");
}

PRUEBA(PruebasHistorial, back_forward_y_topes) {
    BrowserHistory bh("a");
    bh.visit("b");
    bh.visit("c");
    bh.visit("d");
    COMPROBAR(bh.back(1) == "c", "back(1)");
    COMPROBAR(bh.back(2) == "a", "back(2)");
    COMPROBAR(bh.forward(2) == "c", "forward(2)");
    COMPROBAR(bh.back(100) == "a", "back(100) se para en la primera");
    COMPROBAR(bh.forward(100) == "d", "forward(100) se para en la ultima");
    comprobar(bh, {"a", "b", "c", "d"}, "d", "back/forward no borran nada");
}

PRUEBA(PruebasHistorial, visit_descarta_lo_de_delante) {
    BrowserHistory bh("leetcode.com");
    for (const char* u : {"google.com", "facebook.com", "youtube.com"}) bh.visit(u);
    bh.back(1);
    bh.visit("linkedin.com");
    comprobar(bh, {"leetcode.com", "google.com", "facebook.com", "linkedin.com"},
              "linkedin.com", "visit tras back");
    bh.back(10);
    bh.visit("x");
    comprobar(bh, {"leetcode.com", "x"}, "x", "visit desde la primera pagina");
}

PRUEBA(PruebasHistorial, traza_del_enunciado) {
    BrowserHistory bh("leetcode.com");
    bh.visit("google.com");
    bh.visit("facebook.com");
    bh.visit("youtube.com");
    COMPROBAR(bh.back(1) == "facebook.com", "back(1)");
    COMPROBAR(bh.back(1) == "google.com", "back(1)");
    COMPROBAR(bh.forward(1) == "facebook.com", "forward(1)");
    bh.visit("linkedin.com");
    COMPROBAR(bh.forward(2) == "linkedin.com", "forward(2)");
    COMPROBAR(bh.back(2) == "google.com", "back(2)");
    COMPROBAR(bh.back(7) == "leetcode.com", "back(7)");
}

PRUEBA(PruebaContraVector, navegacion_aleatoria) {
    std::mt19937 rng(1472);
    BrowserHistory bh("p0");
    std::vector<std::string> modelo{"p0"};
    int pos = 0;
    for (int paso = 0; paso < 3000; ++paso) {
        int op = rng() % 3, k = rng() % 7;
        std::string tras = "paso " + std::to_string(paso);
        if (op == 0) {
            std::string url = "p" + std::to_string(paso);
            bh.visit(url);
            modelo.resize(pos + 1);
            modelo.push_back(url);
            ++pos;
        } else if (op == 1) {
            pos = std::max(0, pos - k);
            COMPROBAR(bh.back(k) == modelo[pos], tras);
        } else {
            pos = std::min((int)modelo.size() - 1, pos + k);
            COMPROBAR(bh.forward(k) == modelo[pos], tras);
        }
        comprobar(bh, modelo, modelo[pos], tras);
    }
}

PRUEBA(PruebasMemoria, visit_libera_las_paginas_descartadas) {
    int antes = Nodo::vivos;
    {
        BrowserHistory bh("inicio");
        for (int i = 0; i < 100; ++i) bh.visit("p" + std::to_string(i));
        bh.back(100);
        int vivos = Nodo::vivos;
        bh.visit("nueva");                               // descarta 100, crea 1
        COMPROBAR(Nodo::vivos == vivos - 100 + 1,
                  "las paginas descartadas no se han liberado (delete): memory leak");
    }
    COMPROBAR(Nodo::vivos == antes, "al destruir el historial deben liberarse todas las paginas");
}

int main(int argc, char** argv) {
    int resultado = mini_test::ejecutar(argc, argv);
    std::cout << "Nodos vivos al terminar: " << Nodo::vivos
              << (Nodo::vivos == 0 ? "  (sin memory leaks)" : "  <-- MEMORY LEAK") << "\n";
    return resultado;
}
