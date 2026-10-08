# Práctica 3: Listas Doblemente Enlazadas e Historial de Navegador

**Asignatura**: Algoritmia y Estructuras de Datos (AED I) — Bloque I
**Titulación**: Ingeniería Informática – Inteligencia Artificial
**Duración**: 2 h en clase + ~1 h en casa
**Peso**: 10% de la nota del bloque
**Lenguaje**: Python 3.10 o posterior, sin librerías externas (hay una versión opcional en C++17)

> Este es el **enunciado**: qué hay que hacer. La explicación paso a paso está en las diapositivas (`diapositivas/`) y el resumen para tener a mano, en `chuleta.md`.

## Contexto

En la teoría y en el repaso de clase hemos visto la **lista simplemente enlazada**: cada nodo solo conoce al **siguiente**. Eso hace caras dos operaciones: borrar el último nodo y borrar o insertar antes de un nodo dado, porque hay que recorrer la lista para encontrar al anterior.

En esta práctica vas a:

1. Escribir en Python una **lista doblemente enlazada**: la misma lista con un solo puntero más en cada nodo, `anterior`, que convierte esas operaciones en O(1).
2. Hacer que se use **igual que una `list`**: `len(l)`, `for x in l`, `reversed(l)`, `x in l`, `print(l)`.
3. Construir sobre ella una aplicación real: el **historial atrás/adelante de un navegador** (LeetCode #1472), sin tablas hash.

## Ficheros

Trabaja siempre desde la carpeta `python/` (`cd python`). En Windows, si `python3` no existe, usa `python` o `py`.

| Fichero | Qué es | ¿Lo modificas? |
|---------|--------|----------------|
| `python/lista_doble.py` | `NodoDoble` y `ListaDoble`, con huecos (`TODO`) | **Sí** (Partes 1 y 2) |
| `python/historial.py` | `BrowserHistory` sobre tu `ListaDoble`, con huecos | **Sí** (Parte 3) |
| `python/test_lista_doble.py`, `python/test_historial.py` | Pruebas de autocomprobación | No |
| `python/ejemplo_lista.txt`, `python/ejemplo_historial.txt` | Entradas de ejemplo de los dos problemas del juez | No |
| `python/generar_envio.py` | Crea `envio_historial.py` (lista + historial en un solo fichero) para el juez | No |
| `RESPUESTAS.md` | Hoja con la tabla de costes y tres preguntas | **Sí** |
| `chuleta.md` | Resumen de una página: punteros, casos especiales, costes | No |
| `diapositivas/` | Diapositivas de la sesión en PDF | No |
| `python/lista_simple.py`, `python/comparativa.py` | Ampliación opcional: medir con el reloj | No |
| `cpp/` | Ampliación opcional: la misma práctica en C++ | Solo si la haces en C++ |

---

## Parte 1 · Implementar `ListaDoble` (≈ 45 min, en clase)

### La representación

```
    cabeza                              cola
      │                                   │
      ▼                                   ▼
┌───┬────┬───┐    ┌───┬────┬───┐    ┌───┬────┬───┐
│   │ A  │ ●─┼───►│   │ B  │ ●─┼───►│   │ C  │ × │
│ × │    │   │◄───┼─● │    │   │◄───┼─● │    │   │    tamano = 3
└───┴────┴───┘    └───┴────┴───┘    └───┴────┴───┘
```

Cada `NodoDoble` guarda `anterior | dato | siguiente`; la `ListaDoble` guarda `cabeza`, `cola` y `tamano`. `×` es `None`.

Lee el bloque **invariante de la representación** al principio de la clase. Es el contrato interno: cualquier operación puede romperlo mientras trabaja, pero debe dejarlo cierto al terminar. Los tests lo comprueban con `invariante_correcto()` después de **cada** llamada.

- `tamano == 0` ⇔ `cabeza is None` ⇔ `cola is None`.
- Si no está vacía: `cabeza.anterior is None` y `cola.siguiente is None`.
- De `cabeza` a `cola` por `siguiente` hay exactamente `tamano` nodos.
- Para cada nodo `x` que no es la cabeza: `x.anterior.siguiente is x`.

### Qué hay que hacer

`insert_first` ya está hecho como ejemplo (son los 4 punteros de la diapositiva). Completa los métodos marcados con `TODO` **en este orden** y ejecuta el grupo de tests de cada paso:

| Orden | Métodos | Tests |
|-------|---------|-------|
| 1 | `insert_last`, `__reversed__` | `python3 -m unittest -v test_lista_doble.PruebasInsercion` |
| 2 | `insert_before(nodo, dato)`, `insert_after(nodo, dato)` | `... test_lista_doble.PruebasInsercionRelativa` |
| 3 | `delete_node(nodo)`, `delete_first()`, `delete_last()` | `... test_lista_doble.PruebasBorrado` y `... test_lista_doble.PruebaContraList` |

Algunas indicaciones:

- **`__reversed__`** se escribe como `__iter__` (un *generador* con `yield`), pero empezando por la `cola` y siguiendo `anterior`. Es lo que usa `reversed(l)`.
- Los `insert_*` **devuelven el nodo nuevo**: así quien llama ya tiene su referencia (el historial lo necesitará). `l.buscar(dato)` devuelve el nodo de un dato.
- `delete_*` devuelven el dato borrado, como `list.pop()`. Sobre una lista vacía lanzan `IndexError`. `delete_node` deja `nodo.anterior` y `nodo.siguiente` a `None`.
- Empieza por `delete_node`, que es el caso general: `delete_first` y `delete_last` son una línea cada uno.
- El caso que más falla: **la lista vacía** al insertar y **el único elemento** al borrar.
- `PruebaContraList` hace 2000 operaciones aleatorias a la vez sobre tu lista y sobre una `list` y comprueba que coinciden siempre. La `list` hace de **oráculo**: como sabemos que es correcta, sirve para comprobar la nuestra.
- Sustituye cada `O(?)` del código por el coste que consigue tu implementación.

## Parte 2 · ¿Es palíndromo? (≈ 15 min, en clase)

`es_palindromo()`: dos punteros, `inicio = self.cabeza` y `fin = self.cola`, que avanzan hacia el centro. O(n) en tiempo y O(1) en memoria auxiliar. Tests: `test_lista_doble.PruebasPalindromo`.

¿Por qué bastan `tamano // 2` comparaciones? ¿Qué pasa con el elemento central cuando `tamano` es impar?

## Parte 3 · Historial de navegador (≈ 15 min en clase + casa)

En clase vemos la arquitectura y la traza en la pizarra; el código se escribe en casa.

Un navegador guarda las páginas que visitas y te deja ir atrás y adelante. Si estando "atrás" visitas una página nueva, todo lo que había por delante se descarta. Se modela con **tu misma `ListaDoble`**, sin estructuras nuevas (no hace falta ninguna tabla hash: no se busca por nombre, solo se avanza y retrocede). Basta un puntero más, `actual`, al **nodo** en el que estamos:

```
paginas: leetcode.com <-> google.com <-> facebook.com <-> youtube.com
                                              ^
                                            actual
visit("linkedin.com"): se descarta youtube.com, se enlaza linkedin.com
                       detrás de facebook.com y actual pasa a linkedin.com
```

En `historial.py`, el constructor ya crea `self.paginas` (una `ListaDoble`) y `self.actual`. Completa:

| Método | Qué hace | Coste pedido |
|--------|----------|--------------|
| `visit(url)` | Descarta lo que hay por delante de `actual`, enlaza `url` detrás y se mueve a ella | O(1) amortizado |
| `back(steps)` | Retrocede hasta `steps` páginas (o hasta la primera) y devuelve la página actual | O(min(steps, n)) |
| `forward(steps)` | Avanza hasta `steps` páginas (o hasta la última) y devuelve la página actual | O(min(steps, n)) |

Tests: `python3 -m unittest -v test_historial`. Reproducen esta traza:

```
BrowserHistory("leetcode.com")
visit("google.com"); visit("facebook.com"); visit("youtube.com")
back(1)    -> "facebook.com"
back(1)    -> "google.com"
forward(1) -> "facebook.com"
visit("linkedin.com")            se descarta youtube.com
forward(2) -> "linkedin.com"     no hay nada más adelante
back(2)    -> "google.com"
back(7)    -> "leetcode.com"     tope en la primera página
```

> ⚠️ **Error clásico**: hacer `visit()` después de `back()` y no descartar lo que había por delante: `forward()` te llevará a páginas que ya no deberían existir.

## Juez virtual (DOMjudge, en casa)

Plataforma: **https://complicaus.eii.us.es** — dos problemas; en cada uno se sube **un único fichero**:

| Problema | Qué se sube | Cómo probarlo antes |
|----------|-------------|---------------------|
| **Lista doble** | `lista_doble.py`, tal cual | `python3 lista_doble.py < ejemplo_lista.txt` |
| **Historial de navegador** | `envio_historial.py` | `python3 envio_historial.py < ejemplo_historial.txt` |

El historial usa tu `ListaDoble` (`from lista_doble import ListaDoble`) y el juez solo recibe un fichero, así que hay que juntar los dos: `python3 generar_envio.py` crea `envio_historial.py`. No lo edites a mano: si cambias tu código, vuelve a generarlo. La lectura y escritura ya están hechas (`main_lista()` y `main()`): no las toques.

**Problema "Lista doble"**: una orden por línea, los datos son palabras sin espacios.

| Orden | Qué hace | Escribe |
|-------|----------|---------|
| `insert_first X` / `insert_last X` | Inserta X al principio / al final | — |
| `insert_before A X` / `insert_after A X` | Inserta X antes / después del primer A | `ERROR` si no hay A |
| `delete_first` / `delete_last` | Borra el primero / el último | el dato borrado, o `ERROR` si está vacía |
| `delete A` | Borra el primer A | A, o `ERROR` si no hay A |
| `palindromo` | ¿Es palíndromo? | `SI` o `NO` |
| `size` | Tamaño | el número |
| `print` / `print_back` | Recorre hacia delante / hacia atrás | los datos separados por un espacio, o `-` si está vacía |

`print_back` usa tu `__reversed__`: si algún `.anterior` está mal, aquí se nota. Hay casos grandes: un `delete_last` que recorra la lista da **TLE**.

**Problema "Historial de navegador"**: primera línea, la página de inicio; después una orden por línea (`visit URL`, `back K` o `forward K`). Por cada `back` o `forward` se escribe la página en la que te quedas. Con `ejemplo_historial.txt` sale `facebook.com`, `google.com`, `facebook.com`, `linkedin.com`, `google.com`, `leetcode.com` (una por línea).

**Veredictos**: **AC** correcto · **WA** la salida no coincide (¡ojo con mensajes extra!) · **TLE** demasiado lento · **RTE** error en ejecución.

---

## Cierre (en casa, ≈ 10 min)

Rellena `RESPUESTAS.md`: la tabla de costes de tu implementación (deben coincidir con los `O(?)` del código) y tres preguntas cortas.

Antes de entregar:

- [ ] `python3 -m unittest -v test_lista_doble test_historial` pasa (las pruebas de la ampliación salen como *skipped* si no la haces).
- [ ] No queda ningún `O(?)` en el código.
- [ ] El juez da **AC** en los dos problemas (con `envio_historial.py` regenerado a partir de tu versión final).

## Evaluación

| Criterio | Dónde | Puntuación |
|----------|-------|------------|
| Parte 1: operaciones de `ListaDoble` | clase | 5.0 |
| Parte 2: palíndromo | clase | 1.0 |
| Parte 3: Historial de navegador con los costes pedidos | casa | 2.5 |
| `RESPUESTAS.md` | casa | 0.5 |
| Test individual de cierre de sesión | clase | 0.5 |
| Juez automático (AC en los dos problemas) | casa | 0.5 |
| **Total** | | **10.0** |

**Entrega**: un `.zip` con `lista_doble.py`, `historial.py` y `RESPUESTAS.md`, y los envíos con **AC** en el juez.

---

## Ampliación (opcional, no puntúa)

- **Otras operaciones** en `lista_doble.py` (sus tests están en el mismo fichero y se saltan mientras no las hagas):
  - `reverse()`: invertir intercambiando `anterior` y `siguiente` en cada nodo, sin crear nodos. `PruebasReverse`.
  - `intercalar(otra)`: `[1,3,5].intercalar([2,4,6])` → `[1,2,3,4,5,6]`; `otra` no cambia. `PruebasIntercalar`.
  - `rotar(k, derecha=True)`: `[1,2,3,4,5].rotar(2)` → `[4,5,1,2,3]`, sin crear nodos. `PruebasRotar`.
- **Medir con el reloj** (`python3 comparativa.py`): compara tu lista doble con la lista simple del repaso (`lista_simple.py`) y con `list`. Cada tabla mide con *n*, *2n*, *4n*, *8n* y muestra la razón t(2n)/t(n): ≈ 1 es O(1), ≈ 2 es O(n), ≈ 4 es O(n²). Antes de ejecutar, predice la razón de cada columna.
  - **A**: vaciar borrando el último. ¿Cuál sale O(n²) y por qué?
  - **B**: borrar nodos de los que ya tienes la referencia.
  - **C**: recorrer hacia atrás.
  - **D**: bytes por elemento. ¿Cuánto cuesta el puntero `anterior`?
- **La misma práctica en C++** (carpeta `cpp/`), ver abajo.

### Versión en C++

Mismos ejercicios y mismos nombres en `cpp/`: `lista_doble.hpp` (una plantilla `ListaDoble<T>`) e `historial.hpp`, con `TODO`. Compilar y ejecutar las pruebas (desde `cpp/`):

```bash
g++ -std=c++17 -Wall test_lista_doble.cpp -o test_lista && ./test_lista        # o ./test_lista PruebasInsercion
g++ -std=c++17 -Wall test_historial.cpp -o test_historial && ./test_historial
```

En Windows: `.\test_lista.exe`. Cada prueba sale como `ok`, `FALLO`, `PENDIENTE` (aún lanza `TODO`) o `saltada` (ampliación). Diferencias con Python:

- El recorrido hacia atrás es `to_vector_backward()`, y borrar en una lista vacía lanza `std::out_of_range`.
- `delete_*` y `visit()` hacen `delete` de los nodos que quitan.
- **Solo en C++**: destructor, `vaciar()`, constructor de copia y `operator=` (la regla de los tres). Sin ellos hay *memory leaks*: los tests terminan imprimiendo `Nodos vivos al terminar`, que debe ser 0.

Juez en C++: `python3 generar_envio.py` crea `envio_lista.cpp` y `envio_historial.cpp`; súbelos a los mismos dos problemas eligiendo C++. Entrega en C++: `lista_doble.hpp`, `historial.hpp` y `RESPUESTAS.md`.

---

## Recursos

| Recurso | Para qué |
|---------|----------|
| [LeetCode #1472 — Design Browser History](https://leetcode.com/problems/design-browser-history/) | El problema clásico, con juez automático |
| [VisuAlgo — Linked List](https://visualgo.net/en/list) | Animaciones de listas simples y dobles |
| [Python Tutorial — Iteradores y generadores](https://docs.python.org/3/tutorial/classes.html#iterators) | `__iter__`, `__reversed__` y `yield` |

**Siguiente práctica**: Pilas.
