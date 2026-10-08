// lista_doble.hpp
// Practica 3 - Lista doblemente enlazada en C++ (version OPCIONAL; la
// practica se explica en Python, pero puedes entregarla en C++).
//
// Mismos ejercicios y mismos nombres que en Python. Completa los metodos
// marcados con TODO (cada uno lanza ahora std::logic_error("TODO ...")) y
// sustituye cada "O(?)" por el coste que consigue tu implementacion.
//
// Orden de trabajo y grupos de tests (ver README, seccion C++):
//   EN CLASE
//     1. insert_last, to_vector_backward     -> PruebasInsercion
//     2. insert_before, insert_after         -> PruebasInsercionRelativa
//     3. delete_node, delete_first/last      -> PruebasBorrado, PruebaContraVector
//     4. es_palindromo                       -> PruebasPalindromo
//   EN CASA
//     5. reverse                             -> PruebasReverse
//     6. intercalar                          -> PruebasIntercalar
//     7. destructor, vaciar, constructor de
//        copia y operator= (Ejercicio 4)     -> PruebasMemoria
//     8. rotar (reto opcional)               -> PruebasRotar
//
// Compilar y ejecutar los tests (desde la carpeta cpp/):
//   g++ -std=c++17 -Wall test_lista_doble.cpp -o test_lista
//   ./test_lista                      (o ./test_lista PruebasInsercion ...)
#pragma once

#include <initializer_list>
#include <stdexcept>
#include <utility>
#include <vector>

template <typename T>
class ListaDoble {
public:
    struct Nodo {
        T dato;
        Nodo* siguiente;
        Nodo* anterior;
        // Contador de nodos vivos: sube en el constructor y baja en el
        // destructor. Al terminar el programa debe valer 0: si no, hay nodos
        // que nadie ha liberado con delete (memory leak). No lo toques.
        inline static int vivos = 0;

        explicit Nodo(const T& d) : dato(d), siguiente(nullptr), anterior(nullptr) { ++vivos; }
        ~Nodo() { --vivos; }
    };

    // --- Invariante de la representacion -----------------------------------
    //  tamano >= 0
    //  tamano == 0  <=>  cabeza == nullptr  <=>  cola == nullptr
    //  si tamano > 0: cabeza->anterior == nullptr y cola->siguiente == nullptr,
    //    de cabeza a cola por ->siguiente hay exactamente tamano nodos, y
    //    x->anterior->siguiente == x para todo nodo x que no es la cabeza
    // Los tests lo comprueban despues de cada operacion con invariante_correcto().
    // -------------------------------------------------------------------------

    Nodo* cabeza = nullptr;
    Nodo* cola = nullptr;
    int tamano = 0;

    ListaDoble() = default;

    ListaDoble(std::initializer_list<T> datos) {         // ListaDoble<int> l{1, 2, 3};
        for (const T& d : datos) insert_last(d);
    }

    // --- Ejercicio 4 (CASA): la regla de los tres ------------------------------

    ~ListaDoble() {
        // TODO (casa): liberar TODOS los nodos con delete (puedes llamar a vaciar()).
        // Mientras no lo hagas, los tests acabaran con "MEMORY LEAK".
    }

    ListaDoble(const ListaDoble& otra) {
        // Coste: O(?)
        // TODO (casa): copia PROFUNDA: nodos nuevos con los mismos datos.
        // Si copias solo los punteros, las dos listas compartiran nodos y el
        // segundo destructor hara delete de nodos ya liberados.
        (void)otra;
        throw std::logic_error("TODO constructor de copia");
    }

    ListaDoble& operator=(const ListaDoble& otra) {
        // Coste: O(?)
        // TODO (casa): si no es autoasignacion (this != &otra), vaciar y copiar.
        (void)otra;
        throw std::logic_error("TODO operator=");
    }

    void vaciar() {
        // Coste: O(?)
        // TODO (casa): delete de cada nodo y dejar la lista vacia.
        throw std::logic_error("TODO vaciar");
    }

    // --- Consulta ------------------------------------------------------------

    int size() const { return tamano; }
    bool vacia() const { return tamano == 0; }

    Nodo* buscar(const T& dato) const {                  // O(n), primer nodo con dato
        for (Nodo* n = cabeza; n != nullptr; n = n->siguiente)
            if (n->dato == dato) return n;
        return nullptr;
    }

    std::vector<T> to_vector() const {                   // recorrido hacia delante
        std::vector<T> v;
        for (Nodo* n = cabeza; n != nullptr; n = n->siguiente) v.push_back(n->dato);
        return v;
    }

    std::vector<T> to_vector_backward() const {
        // Coste: O(?)
        // TODO: como to_vector, pero empezando por la cola y siguiendo ->anterior.
        throw std::logic_error("TODO to_vector_backward");
    }

    // --- Insercion (todas devuelven el nodo nuevo) ---------------------------

    Nodo* insert_first(const T& dato) {
        // O(1). Hecho como ejemplo: los 4 punteros de la diapositiva.
        Nodo* nuevo = new Nodo(dato);
        if (cabeza == nullptr) {                         // lista vacia: EL caso especial
            cabeza = cola = nuevo;
        } else {
            nuevo->siguiente = cabeza;                   // 1. X.siguiente = cabeza
            // 2. X.anterior = nullptr (ya lo es al crear el nodo)
            cabeza->anterior = nuevo;                    // 3. cabeza.anterior = X
            cabeza = nuevo;                              // 4. cabeza = X
        }
        ++tamano;
        return nuevo;
    }

    Nodo* insert_last(const T& dato) {
        // Coste: O(?)
        // TODO: simetrico a insert_first, trabajando sobre la cola.
        (void)dato;
        throw std::logic_error("TODO insert_last");
    }

    Nodo* insert_before(Nodo* nodo, const T& dato) {
        // Coste: O(?).  pre: nodo es un nodo de ESTA lista.
        // TODO: caso especial -> nodo es la cabeza (usa insert_first).
        (void)nodo; (void)dato;
        throw std::logic_error("TODO insert_before");
    }

    Nodo* insert_after(Nodo* nodo, const T& dato) {
        // Coste: O(?).  pre: nodo es un nodo de ESTA lista.
        // TODO: caso especial -> nodo es la cola (usa insert_last).
        (void)nodo; (void)dato;
        throw std::logic_error("TODO insert_after");
    }

    // --- Borrado ------------------------------------------------------------

    T delete_node(Nodo* nodo) {
        // Coste: O(?).  pre: nodo es un nodo de ESTA lista.
        // TODO: reconectar el enlace izquierdo (o mover cabeza si nodo era la cabeza)
        // TODO: reconectar el enlace derecho (o mover cola si nodo era la cola)
        // TODO: guardar el dato, hacer delete del nodo, actualizar tamano y devolver el dato
        (void)nodo;
        throw std::logic_error("TODO delete_node");
    }

    T delete_first() {
        // Coste: O(?)
        // Si la lista esta vacia: throw std::out_of_range("...").
        // Pista: es un caso particular de delete_node.
        throw std::logic_error("TODO delete_first");
    }

    T delete_last() {
        // Coste: O(?)
        // Si la lista esta vacia: throw std::out_of_range("...").
        throw std::logic_error("TODO delete_last");
    }

    // --- Operaciones sobre la lista entera ------------------------------------

    void reverse() {
        // Coste: O(?). Sin crear nodos.   (CASA)
        // TODO: en cada nodo, std::swap(anterior, siguiente); al final, swap(cabeza, cola).
        throw std::logic_error("TODO reverse");
    }

    bool es_palindromo() const {
        // Coste: O(?) en tiempo y O(?) en memoria auxiliar.
        // TODO: dos punteros (desde cabeza y desde cola) que avanzan hacia el
        //       centro; bastan tamano / 2 comparaciones.
        throw std::logic_error("TODO es_palindromo");
    }

    void intercalar(const ListaDoble& otra) {
        // Coste: O(?)   (CASA, Ejercicio 2). otra NO se modifica.
        //   [1, 3, 5].intercalar([2, 4, 6, 8, 10]) -> [1, 2, 3, 4, 5, 6, 8, 10]
        // TODO: recorre this con un puntero y otra con otro; usa insert_after
        //       sobre el nodo de this y, cuando this se acabe, insert_last.
        (void)otra;
        throw std::logic_error("TODO intercalar");
    }

    void rotar(int k, bool derecha = true) {
        // Coste: O(?). Sin crear nodos.   (reto opcional)
        //   [1,2,3,4,5].rotar(2) -> [4,5,1,2,3];  rotar(2, false) -> [3,4,5,1,2]
        (void)k; (void)derecha;
        throw std::logic_error("TODO rotar");
    }

    // --- Comprobacion explicita del invariante (no se toca) ---------------------

    bool invariante_correcto() const {
        if (tamano < 0) return false;
        if (tamano == 0) return cabeza == nullptr && cola == nullptr;
        if (cabeza == nullptr || cola == nullptr) return false;
        if (cabeza->anterior != nullptr || cola->siguiente != nullptr) return false;
        int contados = 0;
        Nodo* previo = nullptr;
        for (Nodo* n = cabeza; n != nullptr; n = n->siguiente) {
            if (++contados > tamano) return false;       // evita colgarse con un ciclo
            if (n->anterior != previo) return false;
            previo = n;
        }
        return contados == tamano && previo == cola;
    }
};
