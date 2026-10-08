// mini_test.hpp
// Un mini marco de pruebas (sin librerias externas) para la practica.
// No hay que modificarlo.
//
//   PRUEBA(Grupo, nombre) { ... COMPROBAR(condicion, "mensaje"); ... }
//
// El ejecutable de pruebas acepta como argumentos los grupos a ejecutar:
//   ./test_lista PruebasInsercion PruebasBorrado
// Sin argumentos ejecuta todos.
#pragma once

#include <functional>
#include <iostream>
#include <set>
#include <stdexcept>
#include <string>
#include <vector>

namespace mini_test {

struct Fallo : std::runtime_error {
    using std::runtime_error::runtime_error;
};
struct Saltar : std::runtime_error {          // prueba opcional sin implementar
    using std::runtime_error::runtime_error;
};

struct Prueba {
    std::string grupo, nombre;
    std::function<void()> cuerpo;
};

inline std::vector<Prueba>& registro() {
    static std::vector<Prueba> pruebas;
    return pruebas;
}

inline bool registrar(const char* grupo, const char* nombre, std::function<void()> f) {
    registro().push_back({grupo, nombre, std::move(f)});
    return true;
}

// Ejecuta las pruebas de los grupos pedidos. Devuelve 0 si todo ha ido bien.
inline int ejecutar(int argc, char** argv) {
    std::set<std::string> grupos(argv + 1, argv + argc);
    int ok = 0, fallos = 0, pendientes = 0, saltadas = 0;
    for (const Prueba& p : registro()) {
        if (!grupos.empty() && !grupos.count(p.grupo)) continue;
        std::cout << p.grupo << "." << p.nombre << " ... ";
        try {
            p.cuerpo();
            std::cout << "ok\n";
            ++ok;
        } catch (const Saltar& e) {
            std::cout << "saltada (" << e.what() << ")\n";
            ++saltadas;
        } catch (const std::logic_error& e) {
            // Los metodos sin hacer de la plantilla lanzan logic_error("TODO ...")
            if (std::string(e.what()).rfind("TODO", 0) == 0) {
                std::cout << "PENDIENTE (" << e.what() << ")\n";
                ++pendientes;
            } else {
                std::cout << "FALLO\n    excepcion inesperada: " << e.what() << "\n";
                ++fallos;
            }
        } catch (const std::exception& e) {
            std::cout << "FALLO\n    " << e.what() << "\n";
            ++fallos;
        }
    }
    std::cout << "\n" << ok << " ok, " << fallos << " fallos, " << pendientes
              << " pendientes, " << saltadas << " saltadas\n";
    return (fallos || pendientes) ? 1 : 0;
}

}  // namespace mini_test

#define MT_CONCAT2(a, b) a##b
#define MT_CONCAT(a, b) MT_CONCAT2(a, b)
#define PRUEBA(grupo, nombre)                                                        \
    static void grupo##_##nombre();                                                 \
    static bool MT_CONCAT(reg_, __LINE__) =                                         \
        mini_test::registrar(#grupo, #nombre, grupo##_##nombre);                    \
    static void grupo##_##nombre()

#define COMPROBAR(cond, msg)                                                          \
    do {                                                                              \
        if (!(cond))                                                                  \
            throw mini_test::Fallo(std::string(msg) + "  [falla: " #cond "]  (linea " \
                                   + std::to_string(__LINE__) + ")");                 \
    } while (0)
