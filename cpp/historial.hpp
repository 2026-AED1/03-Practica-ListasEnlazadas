// historial.hpp
// Practica 3 - Historial de navegador (LeetCode #1472) sobre TU ListaDoble.
// Trabajo de CASA (Ejercicio 3). Version C++ opcional.
//
// Las paginas van en una ListaDoble<std::string>; 'actual' apunta al NODO de
// la pagina en la que estamos. Sin tablas hash ni estructuras nuevas.
//
// Compilar y ejecutar los tests (desde la carpeta cpp/):
//   g++ -std=c++17 -Wall test_historial.cpp -o test_historial && ./test_historial
#pragma once

#include <stdexcept>
#include <string>

#include "lista_doble.hpp"

class BrowserHistory {
public:
    using Lista = ListaDoble<std::string>;

    Lista paginas;            // de la mas antigua a la mas reciente
    Lista::Nodo* actual;      // invariante: nodo de paginas, nunca nullptr

    explicit BrowserHistory(const std::string& homepage) {
        actual = paginas.insert_last(homepage);
    }

    void visit(const std::string& url) {
        // Coste: O(?)   (pista: "amortizado")
        // TODO:
        // 1. Descartar todas las paginas que hay POR DELANTE de actual,
        //    liberandolas con delete (si solo cortas actual->siguiente, esos
        //    nodos se quedan en memoria para siempre: memory leak). Pista: tu
        //    ListaDoble ya sabe borrar por el final.
        // 2. Enlazar un nodo nuevo con url justo detras de actual.
        // 3. Mover actual a ese nodo nuevo.
        (void)url;
        throw std::logic_error("TODO visit");
    }

    std::string back(int steps) {
        // Coste: O(?)
        // TODO: mientras queden steps y exista actual->anterior, retrocede.
        //       Devuelve actual->dato.
        (void)steps;
        throw std::logic_error("TODO back");
    }

    std::string forward(int steps) {
        // Coste: O(?)
        // TODO: mientras queden steps y exista actual->siguiente, avanza.
        //       Devuelve actual->dato.
        (void)steps;
        throw std::logic_error("TODO forward");
    }
};
