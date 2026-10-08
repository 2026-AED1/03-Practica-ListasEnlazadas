// main_lista.cpp
// Entrada/salida del juez (DOMjudge, problema "Lista doble"). Ya esta hecho:
// no lo toques. Las ordenes son las mismas que en la version Python (README).
//
// Compilar y probar (desde la carpeta cpp/):
//   g++ -std=c++17 -O2 main_lista.cpp -o lista
//   ./lista < ../python/ejemplo_lista.txt
// Para el juez se sube UN fichero: python3 generar_envio.py  ->  envio_lista.cpp

#include <iostream>
#include <sstream>
#include <string>
#include <vector>

#include "lista_doble.hpp"

static std::string unir(const std::vector<std::string>& v) {
    if (v.empty()) return "-";
    std::string s = v[0];
    for (size_t i = 1; i < v.size(); ++i) s += " " + v[i];
    return s;
}

int main() {
    std::ios::sync_with_stdio(false);
    ListaDoble<std::string> l;
    std::string linea, orden, a, x;
    std::ostringstream out;
    while (std::getline(std::cin, linea)) {
        std::istringstream in(linea);
        if (!(in >> orden)) continue;
        if (orden == "insert_first") {
            in >> a;
            l.insert_first(a);
        } else if (orden == "insert_last") {
            in >> a;
            l.insert_last(a);
        } else if (orden == "insert_before" || orden == "insert_after") {
            in >> a >> x;
            auto* nodo = l.buscar(a);
            if (nodo == nullptr) out << "ERROR\n";
            else if (orden == "insert_before") l.insert_before(nodo, x);
            else l.insert_after(nodo, x);
        } else if (orden == "delete_first" || orden == "delete_last") {
            if (l.vacia()) out << "ERROR\n";
            else out << (orden == "delete_first" ? l.delete_first() : l.delete_last()) << "\n";
        } else if (orden == "delete") {
            in >> a;
            auto* nodo = l.buscar(a);
            if (nodo == nullptr) out << "ERROR\n";
            else out << l.delete_node(nodo) << "\n";
        } else if (orden == "palindromo") {
            out << (l.es_palindromo() ? "SI" : "NO") << "\n";
        } else if (orden == "size") {
            out << l.size() << "\n";
        } else if (orden == "print") {
            out << unir(l.to_vector()) << "\n";
        } else if (orden == "print_back") {
            out << unir(l.to_vector_backward()) << "\n";
        }
    }
    std::cout << out.str();
    return 0;
}
