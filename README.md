# Práctica 3: Listas Doblemente Enlazadas e Historial de Navegador

**Asignatura**: Algoritmia y Estructuras de Datos (AED I) — Bloque I
**Titulación**: Ingeniería Informática – Inteligencia Artificial
**Duración**: 2 h en clase + ~2 h en casa
**Peso**: 10% de la nota del bloque
**Lenguaje**: Python 3.10 o posterior, sin librerías externas

> Este es el **enunciado**: qué hay que hacer. La explicación paso a paso de la sesión está en las diapositivas (`diapositivas/`) y el resumen para tener a mano, en `chuleta.md`.

---

## Contenido del repositorio

| Fichero | Qué es | ¿Lo modificas? |
|---------|--------|----------------|
| `python/lista_doble.py` | `NodoDoble` y `ListaDoble`, con huecos (`TODO`) | **Sí** (Ejercicios 1, 2 y 4) |
| `python/historial.py` | `BrowserHistory` sobre tu `ListaDoble`, con huecos | **Sí** (Ejercicio 3) |
| `python/test_lista_doble.py` | Pruebas de autocomprobación de la lista | No |
| `python/test_historial.py` | Pruebas de autocomprobación del historial | No |
| `python/lista_simple.py` | La lista simplemente enlazada del repaso, ya completa | No |
| `python/comparativa.py` | Experimentos de tiempo y memoria (A–E) | No |
| `python/generar_envio.py` | Crea `envio_historial.py` (lista + historial en un solo fichero) para el juez | No |
| `python/ejemplo_lista.txt`, `python/ejemplo_historial.txt` | Entradas de ejemplo de los dos problemas del juez | No |
| `RESPUESTAS.md` | Hoja donde apuntas costes, tablas y respuestas | **Sí** |
| `chuleta.md` | Resumen de una página: punteros, casos especiales, costes | No |
| `diapositivas/` | Diapositivas de la sesión en PDF | No |

Para descargarlo: `git clone <URL del repositorio>` o botón **Code → Download ZIP**.

Trabaja siempre desde la carpeta `python/`:

```bash
cd python
python3 -m unittest -v test_lista_doble          # todas las pruebas de la lista
python3 -m unittest -v test_lista_doble.PruebasInsercion   # solo un grupo
```

En Windows, si `python3` no existe, usa `python` o `py`.

---

## Objetivos

- Entender por qué un segundo puntero (`anterior`) convierte en O(1) operaciones que en una lista simple son O(n): borrar el último, borrar un nodo dado, insertar antes de un nodo.
- Implementar desde cero una lista doblemente enlazada, gestionando bien los 4 punteros en cada inserción y borrado, y comprobarlo con su **invariante**.
- Hacer que la lista se use como cualquier secuencia de Python: `len(l)`, `for x in l`, `reversed(l)`, `x in l`, `print(l)`.
- Aplicar la navegación bidireccional a problemas clásicos (palíndromo, intercalado, rotación).
- Construir una aplicación real sobre la lista: el historial atrás/adelante de un navegador (LeetCode #1472), sin tablas hash.
- Entender qué pasa con la memoria en Python cuando los nodos se apuntan entre sí (ciclos de referencias).

---

## La lista doble en una página

```
Lista simple:   cabeza -> [A|•] -> [B|•] -> [C|/]
Lista doble:    cabeza -> [/|A|•] <-> [•|B|•] <-> [•|C|/] <- cola        tamano = 3
```

Cada `NodoDoble` guarda `dato`, `siguiente` y `anterior`. La `ListaDoble` guarda `cabeza`, `cola` y `tamano`.

### El invariante de la representación

Es el contrato interno de la clase. Cualquier operación puede romperlo mientras trabaja, pero **debe dejarlo cierto al terminar**:

- `tamano >= 0`, y `tamano == 0` ⇔ `cabeza is None` ⇔ `cola is None`.
- Si la lista no está vacía: `cabeza.anterior is None` y `cola.siguiente is None`.
- Siguiendo `siguiente` desde `cabeza` se visitan exactamente `tamano` nodos y el último es `cola`.
- Para cada nodo `x` que no es la cabeza: `x.anterior.siguiente is x` (los enlaces hacia atrás cuadran con los de hacia delante).

El método `invariante_correcto()` ya está escrito y los tests lo llaman **después de cada operación**. Un fallo "invariante roto tras …" quiere decir que el resultado puede parecer correcto, pero la estructura ha quedado mal por dentro (lo típico: un `.anterior` sin actualizar, o `cola` apuntando a un nodo que ya no está).

### Diferencias con C++ que te van a ayudar

- No hay punteros, pero toda variable de Python es una referencia: `nodo.siguiente = otro` hace lo mismo que en C++.
- `None` hace el papel de `nullptr`. Compara siempre con `is None` / `is not None`, y los nodos con `is` (`nodo is self.cabeza`).
- No hay `delete`: cuando un objeto deja de estar referenciado, Python lo libera. Pero cuidado con los ciclos (Ejercicio 4).
- Los métodos con doble guion bajo son los que usa Python por debajo: `len(l)` llama a `l.__len__()`, `for x in l` a `l.__iter__()` y `reversed(l)` a `l.__reversed__()`.

---

## Sesión en clase (2 h)

| Fase | Duración | Actividad |
|------|----------|-----------|
| Motivación y repaso | 20 min | Dónde se usan las listas dobles; repaso de la lista simple; los 4 punteros |
| Ejercicio 1: Programar la lista doble | 30 min | Live coding en Python con la plantilla y los tests |
| Ejercicio 2: ¿Es palíndromo? | 15 min | Implementar, probar y comparar soluciones |
| Ejercicio 3: Operaciones adicionales | 10 min | Discutir `reverse`, `intercalar` y `rotar` (se programan en casa) |
| Ejercicio 4: Historial de navegador | 15 min | Arquitectura y traza en la pizarra (se programa en casa) |
| Cierre y reflexión | 20 min | Qué queda para casa, dudas y **test individual** |

### Ejercicio 1 — `ListaDoble` (en clase)

Completa los métodos de `lista_doble.py` **en este orden**, ejecutando el grupo de tests de cada paso antes de seguir:

| Orden | Métodos | Coste pedido | Tests |
|-------|---------|--------------|-------|
| 1 | `insert_last`, `__reversed__` (`insert_first` ya está hecho como ejemplo) | O(1) / O(1) por paso | `test_lista_doble.PruebasInsercion` |
| 2 | `insert_before(nodo, dato)`, `insert_after(nodo, dato)` | O(1) | `test_lista_doble.PruebasInsercionRelativa` |
| 3 | `delete_node(nodo)`, `delete_first()`, `delete_last()` | O(1) | `test_lista_doble.PruebasBorrado` y `test_lista_doble.PruebaContraList` |

Indicaciones:

- Los `insert_*` **devuelven el nodo nuevo**: así quien llama ya tiene su referencia (el historial lo necesitará).
- `delete_*` devuelven el dato borrado, como `list.pop()`. Sobre una lista vacía lanzan `IndexError`.
- `delete_node` deja `nodo.anterior` y `nodo.siguiente` a `None`: el nodo borrado queda totalmente desenganchado.
- Empieza por `delete_node`, que es el caso general: `delete_first` y `delete_last` son una línea cada uno.
- El caso que más falla: **la lista vacía** al insertar, y **el único elemento** al borrar.
- `PruebaContraList` hace 2000 operaciones aleatorias a la vez sobre tu lista y sobre una `list` de Python, y comprueba que coinciden siempre. La `list` hace de **oráculo**: como sabemos que es correcta, sirve para comprobar la nuestra.
- Sustituye cada `O(?)` del código por el coste que consigue tu implementación.

### Ejercicio 2 — Algoritmos sobre la lista

1. **`es_palindromo()`** (en clase) — dos punteros, uno desde `cabeza` y otro desde `cola`, que avanzan hacia el centro. O(n) en tiempo y O(1) en memoria auxiliar. Tests: `test_lista_doble.PruebasPalindromo`.
   ¿Por qué bastan `tamano // 2` comparaciones? ¿Qué pasa con el elemento central cuando `tamano` es impar?
2. **`intercalar(otra)`** (en casa) — inserta en la lista los datos de `otra` alternándolos; si una es más larga, lo que sobra queda al final. `otra` no se modifica. Tests: `test_lista_doble.PruebasIntercalar`.
   ```
   [1 <-> 3 <-> 5].intercalar([2 <-> 4 <-> 6 <-> 8])  ->  [1 <-> 2 <-> 3 <-> 4 <-> 5 <-> 6 <-> 8]
   ```
   Pista: recorre la lista con un puntero y `otra` con un `for`; usa `insert_after` sobre el nodo actual y, cuando la lista se acabe, `insert_last`.

### Ejercicio 3 — Historial de navegador (arquitectura en clase, código en casa)

Un navegador guarda las páginas que visitas y te deja ir atrás y adelante. Si estando "atrás" visitas una página nueva, todo lo que había por delante se descarta (el botón "adelante" se pone gris).

Se modela con **la misma `ListaDoble`**, sin ninguna estructura nueva (ni diccionario ni tabla hash: no hay que buscar páginas por nombre, solo moverse de forma secuencial). Basta con un puntero más, `actual`, que indica en qué **nodo** estamos:

```
paginas: leetcode.com <-> google.com <-> facebook.com <-> youtube.com
                                              ^
                                            actual

visit("linkedin.com") desde aquí:
  1. youtube.com se descarta (estaba por delante)
  2. se enlaza un nodo nuevo linkedin.com justo después de facebook.com
  3. actual pasa a apuntar a linkedin.com

paginas: leetcode.com <-> google.com <-> facebook.com <-> linkedin.com
                                                              ^
                                                            actual
```

En `historial.py`, el constructor ya crea `self.paginas` (una `ListaDoble`) y `self.actual`. Completa:

| Método | Qué hace | Coste pedido |
|--------|----------|--------------|
| `visit(url)` | Descarta todo lo que hay por delante de `actual`, enlaza `url` detrás y se mueve a ella | O(1) amortizado |
| `back(steps)` | Retrocede hasta `steps` páginas (o hasta la primera) y devuelve la página actual | O(min(steps, n)) |
| `forward(steps)` | Avanza hasta `steps` páginas (o hasta la última) y devuelve la página actual | O(min(steps, n)) |

Traza que deben reproducir los tests (`python3 -m unittest -v test_historial`):

```
BrowserHistory("leetcode.com")   actual = leetcode.com
visit("google.com")              leetcode.com <-> google.com
visit("facebook.com")            ... <-> google.com <-> facebook.com
visit("youtube.com")             ... <-> facebook.com <-> youtube.com
back(1)    -> "facebook.com"
back(1)    -> "google.com"
forward(1) -> "facebook.com"
visit("linkedin.com")            se descarta youtube.com
forward(2) -> "linkedin.com"     no hay nada más adelante
back(2)    -> "google.com"
back(7)    -> "leetcode.com"     tope en la primera página
```

¿Por qué "O(1) **amortizado**" para `visit`? Descartar k páginas cuesta O(k), pero cada página se descarta como mucho una vez en toda la vida del historial.

> ⚠️ **Error clásico**: hacer `visit()` después de `back()` y olvidar que `actual.siguiente` ya apuntaba a algo. Si el historial "hacia adelante" no se descarta bien, `forward()` te llevará a páginas que ya no deberían existir.

### Ejercicio 4 — Memoria en Python: ciclos de referencias (en casa)

Python libera un objeto en cuanto nadie lo referencia (**contador de referencias**). Pero en una lista doble cada par de vecinos se apuntan entre sí: `A.siguiente is B` y `B.anterior is A`. Eso es un **ciclo**, y un ciclo nunca llega a cero referencias aunque nadie de fuera lo use. Esos nodos solo los libera el **recolector de ciclos** (`gc`), que pasa de vez en cuando y tiene que examinar los objetos uno a uno.

Es el equivalente en Python de los *memory leaks* de C++: no rompe el programa, pero la memoria no se libera cuando debería. Para verlo, `NodoDoble` lleva un contador de nodos vivos (`NodoDoble.vivos`), igual que el contador estático que se usa en C++, y los tests apagan el recolector de ciclos con `gc.disable()`.

Completa en `lista_doble.py`, y comprueba con `test_lista_doble.PruebasMemoria`:

- `vaciar()` — deja la lista vacía **rompiendo todos los enlaces** entre nodos, para que cada nodo se libere al instante. Es el equivalente al destructor de C++. Coste O(n).
- `copiar()` — devuelve una lista nueva con nodos nuevos y los mismos datos (*deep copy*, como el constructor de copia de C++). Recuerda: en Python `b = a` **no copia nada**, solo da otro nombre a la misma lista.

Y en `historial.py`, `visit()` debe dejar las páginas descartadas **desenganchadas** (`test_historial.PruebasMemoria`). Si solo cortas `actual.siguiente`, las páginas descartadas siguen apuntándose entre sí y forman un ciclo.

### Reto opcional — `rotar(k, derecha=True)`

Rota la lista k posiciones sin crear nodos nuevos: `[1,2,3,4,5].rotar(2)` → `[4,5,1,2,3]`. Pista: normaliza `k %= tamano`, localiza el nodo que será la nueva cola y reconecta cabeza y cola. No puntúa aparte, pero es una pregunta típica de entrevista técnica. Tests: `test_lista_doble.PruebasRotar` (se saltan si no lo implementas).

---

## Trabajo en casa (~2 h)

No se hace en el laboratorio, pero es tan obligatorio como lo anterior: se evalúa en la entrega de código.

| Tarea | Tiempo estimado | Tests |
|-------|-----------------|-------|
| `reverse()`: invertir intercambiando `anterior` y `siguiente` en cada nodo, O(n), sin crear nodos | 10 min | `PruebasReverse` |
| `intercalar(otra)` | 20 min | `PruebasIntercalar` |
| `BrowserHistory`: `visit`, `back`, `forward` | 30 min | `test_historial` |
| Ejercicio 4: `vaciar`, `copiar` y `visit` sin ciclos | 15 min | `PruebasMemoria` (en los dos ficheros) |
| Experimentos de `comparativa.py` y hoja `RESPUESTAS.md` | 30 min | — |
| Enviar los dos problemas al juez | 10 min | — |
| `rotar(k)` — reto opcional | (opcional) | `PruebasRotar` |

Cuando todo esté hecho, esto tiene que salir sin fallos:

```bash
python3 -m unittest -v test_lista_doble test_historial
```

---

## Medir: la teoría contra el reloj (en casa)

El tiempo absoluto depende de tu ordenador, así que no nos interesa. Lo que nos interesa es **cómo crece**. Cada experimento mide con *n*, *2n*, *4n* y *8n* y muestra la razón t(2n)/t(n):

| Razón | Significa |
|-------|-----------|
| ≈ 1 | O(1): el coste no depende de *n* |
| ≈ 2 | O(n) |
| ≈ 4 | O(n²) |

```bash
python3 comparativa.py A          # uno
python3 comparativa.py B C        # varios
python3 comparativa.py            # todos (alrededor de un minuto)
```

**Antes de ejecutar cada experimento**, apunta en `RESPUESTAS.md` qué razón esperas en cada columna. Después ejecútalo, copia la tabla y explica las diferencias.

- **A · Vaciar borrando el último.** `ListaSimple.delete_last` frente a `ListaDoble.delete_last` y `list.pop()`. ¿Cuál es O(n²) en total y por qué? ¿Qué puntero lo arregla?
- **B · Borrar nodos de los que ya tenemos la referencia.** ¿Por qué la lista simple no puede aprovechar que ya tiene el nodo? ¿Qué hace `list.remove(x)` que lo hace O(n)?
- **C · Recorrer hacia atrás.** ¿Por qué la lista simple sale cuadrática? ¿Qué método de tu clase hace que `reversed(l)` sea O(n)?
- **D · Memoria por elemento.** ¿Cuánto ocupa cada nodo de la lista simple y de la doble? ¿Cuánto cuesta el puntero `anterior`? Compáralo con una `list`. (Recuerda el mensaje de la práctica: *pagar memoria para ganar velocidad*.)
- **E · Nodos descartados y recolector de ciclos.** ¿Por qué tras `del lista` siguen vivos todos los nodos? ¿Qué cambia con `vaciar()`? ¿Y con tu `visit()`?

---

## Juez virtual (DOMjudge)

Plataforma: **https://complicaus.eii.us.es** — dos problemas, y en cada uno se sube **un único fichero**:

| Problema | Qué se sube | Cómo probarlo antes |
|----------|-------------|---------------------|
| **Lista doble** | `lista_doble.py`, tal cual | `python3 lista_doble.py < ejemplo_lista.txt` |
| **Historial de navegador** | `envio_historial.py` (ver abajo) | `python3 envio_historial.py < ejemplo_historial.txt` |

La lectura de la entrada y la escritura de la salida ya están hechas (`main_lista()` en `lista_doble.py` y `main()` en `historial.py`): no las toques.

**¿Por qué el historial necesita otro fichero?** Porque el historial está construido sobre tu `ListaDoble`: `historial.py` hace `from lista_doble import ListaDoble`. El juez solo recibe un fichero, así que hay que juntar los dos. Lo hace un script:

```bash
python3 generar_envio.py      # crea envio_historial.py = lista_doble.py + historial.py
```

No edites `envio_historial.py` a mano: si cambias tu código, vuelve a generarlo.

### Problema "Lista doble"

Una orden por línea; los datos son palabras sin espacios.

| Orden | Qué hace | Escribe |
|-------|----------|---------|
| `insert_first X` / `insert_last X` | Inserta X al principio / al final | — |
| `insert_before A X` / `insert_after A X` | Inserta X antes / después del primer A | `ERROR` si no hay A |
| `delete_first` / `delete_last` | Borra el primero / el último | el dato borrado, o `ERROR` si está vacía |
| `delete A` | Borra el primer A | A, o `ERROR` si no hay A |
| `reverse` | Invierte la lista | — |
| `intercalar X Y Z …` | Intercala la lista con `[X, Y, Z, …]` | — |
| `palindromo` | ¿Es palíndromo? | `SI` o `NO` |
| `size` | Tamaño | el número |
| `print` / `print_back` | Recorre hacia delante / hacia atrás | los datos separados por un espacio, o `-` si está vacía |

`print_back` usa tu `__reversed__`: si algún `.anterior` está mal, aquí se nota. Ojo: hay casos grandes, y un `delete_last` que recorra la lista da **TLE**.

### Problema "Historial de navegador"

| Entrada (stdin) | Salida (stdout) |
|-----------------|-----------------|
| Primera línea: página de inicio.<br>Después, una orden por línea: `visit URL`, `back K` o `forward K`. | Por cada `back` o `forward`, la página en la que te quedas. |

Con `ejemplo_historial.txt` la salida debe ser:

```
facebook.com
google.com
facebook.com
linkedin.com
google.com
leetcode.com
```

**Veredictos del juez**: **AC** correcto · **WA** la salida no coincide (¡ojo con mensajes extra!) · **TLE** demasiado lento (¿`back` recorre más de lo que debe?) · **RTE** error en ejecución.

---

## Errores comunes

| Síntoma | Causa probable |
|---------|----------------|
| `AttributeError: 'NoneType' object has no attribute 'siguiente'` | No se trató la lista vacía, o un nodo en un extremo, antes de usar `.anterior`/`.siguiente` |
| "invariante roto" tras borrar el único elemento | `cabeza` o `cola` siguen apuntando al nodo borrado |
| `reversed(l)` no da la lista al revés, pero `list(l)` está bien | Algún `.anterior` no se actualizó al insertar o borrar |
| El palíndromo falla en listas de tamaño par | Se usó `tamano // 2 + 1` y se comparó un nodo consigo mismo… o se avanzó un solo puntero |
| `reverse()` deja `cabeza`/`cola` mal | Se intercambiaron los punteros de cada nodo pero no `cabeza` y `cola` |
| El historial no descarta bien las páginas tras `back()` + `visit()` | No se sobrescribió lo que había detrás de `actual` |
| `PruebasMemoria` dice que siguen vivos nodos | Quedan nodos descartados que se apuntan entre sí (ciclo) |

---

## Checklists

**Antes de salir de clase**
- [ ] Pasan `PruebasInsercion`, `PruebasInsercionRelativa`, `PruebasBorrado`, `PruebaContraList` y `PruebasPalindromo`.
- [ ] Sé explicar los 4 punteros de una inserción y los 3 casos especiales de `delete_node`.
- [ ] Entiendo la traza del historial (puntero `actual`) lo bastante como para programarla en casa sin ayuda.
- [ ] Sé exactamente qué me llevo para casa.

**Antes de entregar**
- [ ] `python3 -m unittest -v test_lista_doble test_historial` pasa entero (salvo `PruebasRotar`, que es opcional).
- [ ] No queda ningún `O(?)` en el código.
- [ ] `RESPUESTAS.md` tiene la tabla de costes, las predicciones, las tablas de `comparativa.py` y las respuestas.
- [ ] El juez da **AC** en los dos problemas (con `envio_historial.py` regenerado a partir de la versión final).

---

## Evaluación

| Criterio | Cuándo se trabaja | Puntuación |
|----------|-------------------|------------|
| Ejercicio 1: operaciones de `ListaDoble` (incluido `reverse`) | clase + casa | 4.0 |
| Ejercicio 2: palíndromo e intercalado | clase + casa | 1.5 |
| Ejercicio 3: Historial de navegador con los costes pedidos | casa | 2.5 |
| Ejercicio 4: memoria (`vaciar`, `copiar`, `visit` sin ciclos) y hoja `RESPUESTAS.md` | casa | 1.0 |
| Test individual de cierre de sesión | clase | 0.5 |
| Juez automático (AC en los dos problemas) | casa | 0.5 |
| **Total** | | **10.0** |

## Entregables

1. 🏫 Al terminar la sesión: el test individual (20 preguntas), sin acceso a internet.
2. 🏠 Antes de la fecha límite, subido a la plataforma: un `.zip` con `lista_doble.py`, `historial.py` y `RESPUESTAS.md`.
3. 🏠 Envíos con veredicto **AC** en los dos problemas del juez.

---

## Recursos

| Recurso | Para qué |
|---------|----------|
| [LeetCode #1472 — Design Browser History](https://leetcode.com/problems/design-browser-history/) | El problema clásico, con juez automático |
| [VisuAlgo — Linked List](https://visualgo.net/en/list) | Animaciones de listas simples y dobles |
| [Python Tutorial — Clases e iteradores](https://docs.python.org/3/tutorial/classes.html#iterators) | `__iter__`, generadores y `yield` |
| [Python — módulo `gc`](https://docs.python.org/3/library/gc.html) | El recolector de ciclos |

---

**Siguiente práctica**: Pilas — implementación y aplicaciones (evaluación de expresiones, deshacer/rehacer, backtracking).
