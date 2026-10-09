// test_lista_doble.cpp
// Pruebas de autocomprobacion de la ListaDoble en C++. No hay que modificarlo.
//
// Todas las pruebas comprueban, ademas del resultado, el INVARIANTE de la
// representacion y el recorrido en los dos sentidos (el de atras, en cuanto
// to_vector_backward esta hecho; mientras no, solo falla recorrido_hacia_atras).
//
// Compilar (desde la carpeta cpp/):
//   g++ -std=c++17 -Wall test_lista_doble.cpp -o test_lista
// Ejecutar todo, o solo algunos grupos:
//   ./test_lista
//   ./test_lista PruebasInsercion PruebasBorrado
// Grupos, en el orden de trabajo:
//   obligatorio: PruebasInsercion PruebasInsercionRelativa PruebasBorrado
//                PruebaContraVector PruebasPalindromo PruebasMemoria
//   ampliacion:  PruebasReverse PruebasIntercalar PruebasRotar (opcional)

#include <algorithm>
#include <random>
#include <string>
#include <vector>

#include "lista_doble.hpp"
#include "mini_test.hpp"

using Lista = ListaDoble<int>;
using ListaS = ListaDoble<std::string>;

template <typename T>
static void comprobar(const ListaDoble<T>& l, std::vector<T> esperado, const std::string& tras) {
    COMPROBAR(l.invariante_correcto(), "invariante roto tras " + tras);
    COMPROBAR(l.size() == (int)esperado.size(), "tamano tras " + tras);
    COMPROBAR(l.to_vector() == esperado, "recorrido hacia delante tras " + tras);
    std::vector<T> atras;
    try {
        atras = l.to_vector_backward();
    } catch (const std::logic_error& e) {
        // to_vector_backward sigue en TODO (paso 1): de momento no se comprueba
        // aqui; lo comprueba PruebasInsercion.recorrido_hacia_atras.
        if (std::string(e.what()).rfind("TODO", 0) == 0) return;
        throw;
    }
    std::reverse(esperado.begin(), esperado.end());
    COMPROBAR(atras == esperado, "recorrido hacia atras tras " + tras);
}

static int vivos() { return Lista::Nodo::vivos + ListaS::Nodo::vivos; }

// Ejecuta una operacion de la ampliacion; si sigue en TODO, la prueba se salta.
template <typename F>
static void opcional(F f) {
    try {
        f();
    } catch (const std::logic_error& e) {
        if (std::string(e.what()).rfind("TODO", 0) == 0) throw mini_test::Saltar("ampliacion opcional");
        throw;
    }
}

// ---------------------------------------------------------------- insercion

PRUEBA(PruebasInsercion, lista_nueva_vacia) {
    Lista l;
    COMPROBAR(l.vacia(), "una lista nueva debe estar vacia");
    comprobar(l, {}, "crear");
}

PRUEBA(PruebasInsercion, insert_last) {
    Lista l;
    for (int v : {10, 20, 30}) l.insert_last(v);
    comprobar(l, {10, 20, 30}, "insert_last");
    COMPROBAR(l.cola->anterior->dato == 20, "cola->anterior");
}

PRUEBA(PruebasInsercion, recorrido_hacia_atras) {
    Lista vacia;
    COMPROBAR(vacia.to_vector_backward().empty(), "recorrido hacia atras de una lista vacia");
    Lista l;
    for (int v : {1, 2, 3}) l.insert_first(v);
    COMPROBAR(l.to_vector_backward() == std::vector<int>({1, 2, 3}), "recorrido hacia atras");
}

PRUEBA(PruebasInsercion, insert_first) {
    Lista l;
    for (int v : {1, 2, 3}) l.insert_first(v);
    comprobar(l, {3, 2, 1}, "insert_first");
}

PRUEBA(PruebasInsercion, primera_insercion_en_lista_vacia) {
    Lista a, b;
    a.insert_first(7);
    b.insert_last(7);
    COMPROBAR(a.cabeza == a.cola && b.cabeza == b.cola, "con un elemento, cabeza == cola");
    comprobar(a, {7}, "insert_first en lista vacia");
    comprobar(b, {7}, "insert_last en lista vacia");
}

PRUEBA(PruebasInsercion, mezcla_y_nodo_devuelto) {
    Lista l;
    Lista::Nodo* n = l.insert_last(10);
    COMPROBAR(n == l.cola && n->dato == 10, "insert_last debe devolver el nodo nuevo");
    l.insert_last(20);
    COMPROBAR(l.insert_first(5) == l.cabeza, "insert_first debe devolver el nodo nuevo");
    comprobar(l, {5, 10, 20}, "mezclar inserciones");
}

// ---------------------------------------------------------------- insercion relativa

PRUEBA(PruebasInsercionRelativa, insert_before) {
    ListaS l{"A", "C"};
    COMPROBAR(l.insert_before(l.buscar("C"), "B")->dato == "B", "devuelve el nodo nuevo");
    comprobar<std::string>(l, {"A", "B", "C"}, "insert_before en medio");
    l.insert_before(l.cabeza, "inicio");
    comprobar<std::string>(l, {"inicio", "A", "B", "C"}, "insert_before(cabeza)");
}

PRUEBA(PruebasInsercionRelativa, insert_after) {
    ListaS l{"A", "C"};
    COMPROBAR(l.insert_after(l.buscar("A"), "B")->dato == "B", "devuelve el nodo nuevo");
    comprobar<std::string>(l, {"A", "B", "C"}, "insert_after en medio");
    l.insert_after(l.cola, "fin");
    comprobar<std::string>(l, {"A", "B", "C", "fin"}, "insert_after(cola)");
}

PRUEBA(PruebasInsercionRelativa, alrededor_de_un_unico_nodo) {
    Lista l{5};
    l.insert_before(l.cabeza, 4);
    l.insert_after(l.cola, 6);
    comprobar(l, {4, 5, 6}, "insert_before/after con un solo nodo");
}

// ---------------------------------------------------------------- borrado

PRUEBA(PruebasBorrado, delete_first_y_last) {
    Lista l{1, 2, 3};
    COMPROBAR(l.delete_first() == 1, "delete_first devuelve el dato");
    comprobar(l, {2, 3}, "delete_first");
    COMPROBAR(l.delete_last() == 3, "delete_last devuelve el dato");
    comprobar(l, {2}, "delete_last");
}

PRUEBA(PruebasBorrado, delete_node) {
    ListaS l{"A", "B", "C"};
    COMPROBAR(l.delete_node(l.buscar("B")) == "B", "delete_node devuelve el dato");
    comprobar<std::string>(l, {"A", "C"}, "delete_node en medio");
    l.delete_node(l.cabeza);
    comprobar<std::string>(l, {"C"}, "delete_node(cabeza)");
    l.delete_node(l.cola);
    comprobar<std::string>(l, {}, "delete_node del unico elemento");
}

PRUEBA(PruebasBorrado, vaciar_y_reutilizar) {
    for (int modo = 0; modo < 4; ++modo) {
        Lista l{7};
        if (modo % 2) l.delete_last(); else l.delete_first();
        comprobar(l, {}, "borrar el unico elemento");
        if (modo < 2) l.insert_last(8); else l.insert_first(8);
        comprobar(l, {8}, "insertar tras vaciar");
    }
}

PRUEBA(PruebasBorrado, borrar_en_vacia_lanza_out_of_range) {
    Lista l;
    bool lanzo = false;
    try { l.delete_first(); } catch (const std::out_of_range&) { lanzo = true; }
    COMPROBAR(lanzo, "delete_first en lista vacia debe lanzar std::out_of_range");
    lanzo = false;
    try { l.delete_last(); } catch (const std::out_of_range&) { lanzo = true; }
    COMPROBAR(lanzo, "delete_last en lista vacia debe lanzar std::out_of_range");
}

PRUEBA(PruebasBorrado, borrar_libera_el_nodo) {
    int antes = vivos();
    Lista l{1, 2, 3};
    l.delete_node(l.cabeza->siguiente);
    l.delete_first();
    COMPROBAR(vivos() == antes + 1, "cada borrado debe hacer delete del nodo");
}

// ---------------------------------------------------------------- oraculo

PRUEBA(PruebaContraVector, operaciones_aleatorias) {
    // std::vector como ORACULO: mismas operaciones aleatorias en las dos estructuras.
    std::mt19937 rng(2026);
    Lista l;
    std::vector<int> modelo;
    bool reverse_hecho = true;
    for (int paso = 0; paso < 2000; ++paso) {
        int op = rng() % 8, v = rng() % 100;
        std::string tras = "paso " + std::to_string(paso) + " (op " + std::to_string(op) + ")";
        if (op == 0) { l.insert_first(v); modelo.insert(modelo.begin(), v); }
        else if (op == 1) { l.insert_last(v); modelo.push_back(v); }
        else if (op == 2 && !modelo.empty()) {
            COMPROBAR(l.delete_first() == modelo.front(), tras);
            modelo.erase(modelo.begin());
        } else if (op == 3 && !modelo.empty()) {
            COMPROBAR(l.delete_last() == modelo.back(), tras);
            modelo.pop_back();
        } else if (op >= 4 && op <= 6 && !modelo.empty()) {
            int i = rng() % modelo.size();
            Lista::Nodo* n = l.cabeza;
            for (int k = 0; k < i; ++k) n = n->siguiente;
            if (op == 4) { l.insert_before(n, v); modelo.insert(modelo.begin() + i, v); }
            else if (op == 5) { l.insert_after(n, v); modelo.insert(modelo.begin() + i + 1, v); }
            else { COMPROBAR(l.delete_node(n) == modelo[i], tras); modelo.erase(modelo.begin() + i); }
        } else if (op == 7 && reverse_hecho && rng() % 5 == 0) {
            try {                                   // reverse se hace en casa
                l.reverse();
                std::reverse(modelo.begin(), modelo.end());
            } catch (const std::logic_error&) { reverse_hecho = false; }
        }
        comprobar(l, modelo, tras);
    }
}

// ---------------------------------------------------------------- palindromo

PRUEBA(PruebasPalindromo, palindromos) {
    std::vector<std::vector<int>> si = {{}, {1}, {1, 1}, {1, 2, 1}, {1, 2, 2, 1}, {1, 2, 3, 2, 1}};
    for (auto& v : si) {
        Lista l;
        for (int x : v) l.insert_last(x);
        COMPROBAR(l.es_palindromo(), "deberia ser palindromo");
        comprobar(l, v, "es_palindromo (no debe modificar la lista)");
    }
}

PRUEBA(PruebasPalindromo, no_palindromos) {
    std::vector<std::vector<int>> no = {{1, 2}, {1, 2, 3}, {1, 2, 3, 4, 5}, {1, 2, 3, 1}};
    for (auto& v : no) {
        Lista l;
        for (int x : v) l.insert_last(x);
        COMPROBAR(!l.es_palindromo(), "no deberia ser palindromo");
    }
}

// ---------------------------------------------------------------- reverse (ampliacion)

PRUEBA(PruebasReverse, reverse) {
    std::vector<std::vector<int>> casos = {{}, {1}, {1, 2}, {1, 2, 3, 4, 5}};
    for (auto v : casos) {
        Lista l;
        for (int x : v) l.insert_last(x);
        opcional([&] { l.reverse(); });
        std::reverse(v.begin(), v.end());
        comprobar(l, v, "reverse");
    }
}

PRUEBA(PruebasReverse, no_crea_nodos_y_permite_insertar) {
    Lista l{1, 2, 3};
    Lista::Nodo* primero = l.cabeza;
    int antes = vivos();
    opcional([&] { l.reverse(); });
    COMPROBAR(vivos() == antes && l.cola == primero, "reverse no debe crear ni borrar nodos");
    l.insert_last(0);
    l.insert_first(4);
    comprobar(l, {4, 3, 2, 1, 0}, "insertar tras reverse");
}

// ---------------------------------------------------------------- intercalar (ampliacion)

static void caso_intercalar(std::vector<int> a, std::vector<int> b, std::vector<int> esperado) {
    Lista la, lb;
    for (int x : a) la.insert_last(x);
    for (int x : b) lb.insert_last(x);
    opcional([&] { la.intercalar(lb); });
    comprobar(la, esperado, "intercalar");
    comprobar(lb, b, "intercalar (la otra lista no debe cambiar)");
    la.insert_last(99);
    esperado.push_back(99);
    comprobar(la, esperado, "insert_last tras intercalar");
}

PRUEBA(PruebasIntercalar, misma_longitud) { caso_intercalar({1, 3, 5}, {2, 4, 6}, {1, 2, 3, 4, 5, 6}); }
PRUEBA(PruebasIntercalar, otra_mas_larga) { caso_intercalar({1, 3}, {2, 4, 6, 8}, {1, 2, 3, 4, 6, 8}); }
PRUEBA(PruebasIntercalar, otra_mas_corta) { caso_intercalar({1, 3, 5, 7}, {2}, {1, 2, 3, 5, 7}); }
PRUEBA(PruebasIntercalar, vacias) {
    caso_intercalar({}, {1, 2}, {1, 2});
    caso_intercalar({1, 2}, {}, {1, 2});
    caso_intercalar({}, {}, {});
}

// ---------------------------------------------------------------- memoria (solo C++)

PRUEBA(PruebasMemoria, destructor_libera_todo) {
    int antes = vivos();
    {
        Lista l;
        for (int i = 0; i < 1000; ++i) l.insert_last(i);
        COMPROBAR(vivos() == antes + 1000, "1000 nodos creados");
    }   // aqui se ejecuta el destructor
    COMPROBAR(vivos() == antes, "el destructor debe hacer delete de todos los nodos");
}

PRUEBA(PruebasMemoria, vaciar) {
    int antes = vivos();
    Lista l{1, 2, 3};
    l.vaciar();
    comprobar(l, {}, "vaciar");
    COMPROBAR(vivos() == antes, "vaciar debe liberar los nodos");
    l.insert_last(4);
    comprobar(l, {4}, "insertar tras vaciar");
}

PRUEBA(PruebasMemoria, constructor_de_copia_profundo) {
    int antes = vivos();
    {
        Lista a{1, 2, 3};
        Lista b(a);
        COMPROBAR(b.cabeza != a.cabeza, "la copia no debe compartir nodos con el original");
        b.insert_last(4);
        a.delete_first();
        comprobar(a, {2, 3}, "modificar el original");
        comprobar(b, {1, 2, 3, 4}, "modificar la copia");
    }   // si comparten nodos, aqui se hace delete dos veces del mismo nodo
    COMPROBAR(vivos() == antes, "nodos sin liberar tras destruir original y copia");
}

PRUEBA(PruebasMemoria, operador_asignacion) {
    int antes = vivos();
    {
        Lista a{1, 2, 3}, b{9, 9};
        b = a;
        comprobar(b, {1, 2, 3}, "b = a");
        COMPROBAR(b.cabeza != a.cabeza, "b = a no debe compartir nodos");
        b = b;                                          // autoasignacion
        comprobar(b, {1, 2, 3}, "b = b");
    }
    COMPROBAR(vivos() == antes, "nodos sin liberar: operator= debe vaciar antes de copiar");
}

// ---------------------------------------------------------------- rotar (opcional)

static void rotar_y_comprobar(std::vector<int> v, int k, bool derecha, std::vector<int> esperado) {
    Lista l;
    for (int x : v) l.insert_last(x);
    opcional([&] { l.rotar(k, derecha); });
    comprobar(l, esperado, "rotar(" + std::to_string(k) + (derecha ? ")" : ", false)"));
}

PRUEBA(PruebasRotar, derecha_e_izquierda) {
    rotar_y_comprobar({1, 2, 3, 4, 5}, 2, true, {4, 5, 1, 2, 3});
    rotar_y_comprobar({1, 2, 3, 4, 5}, 7, true, {4, 5, 1, 2, 3});
    rotar_y_comprobar({1, 2, 3, 4, 5}, 5, true, {1, 2, 3, 4, 5});
    rotar_y_comprobar({1, 2, 3, 4, 5}, 2, false, {3, 4, 5, 1, 2});
    rotar_y_comprobar({}, 3, true, {});
    rotar_y_comprobar({1}, 3, true, {1});
}

int main(int argc, char** argv) {
    int resultado = mini_test::ejecutar(argc, argv);
    std::cout << "Nodos vivos al terminar: " << vivos()
              << (vivos() == 0 ? "  (sin memory leaks)" : "  <-- MEMORY LEAK") << "\n";
    return resultado;
}
