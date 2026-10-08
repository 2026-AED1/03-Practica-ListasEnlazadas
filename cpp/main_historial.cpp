// main_historial.cpp
// Entrada/salida del juez (DOMjudge, problema "Historial de navegador").
// Ya esta hecho: no lo toques.
//
// Compilar y probar (desde la carpeta cpp/):
//   g++ -std=c++17 -O2 main_historial.cpp -o historial
//   ./historial < ../python/ejemplo_historial.txt
// Para el juez se sube UN fichero: python3 generar_envio.py  ->  envio_historial.cpp

#include <iostream>
#include <sstream>
#include <string>

#include "historial.hpp"

int main() {
    std::ios::sync_with_stdio(false);
    std::string linea, orden, arg;
    if (!std::getline(std::cin, linea)) return 0;
    std::istringstream primera(linea);
    primera >> arg;
    BrowserHistory bh(arg);
    std::ostringstream out;
    while (std::getline(std::cin, linea)) {
        std::istringstream in(linea);
        if (!(in >> orden >> arg)) continue;
        if (orden == "visit") bh.visit(arg);
        else if (orden == "back") out << bh.back(std::stoi(arg)) << "\n";
        else if (orden == "forward") out << bh.forward(std::stoi(arg)) << "\n";
    }
    std::cout << out.str();
    return 0;
}
