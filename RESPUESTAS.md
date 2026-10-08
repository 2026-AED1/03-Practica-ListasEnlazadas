# Práctica 3 · Hoja de respuestas

**Nombre(s):**

## 1 · Costes de tu implementación

Deben coincidir con los `O(?)` que has sustituido en el código.

| Operación | `ListaSimple` (repaso) | Tu `ListaDoble` |
|-----------|------------------------|-----------------|
| `insert_first` | O(1) | |
| `insert_last` | O(1) (con puntero a cola) | |
| `insert_before(nodo, x)` | O(n) | |
| `insert_after(nodo, x)` | O(1) | |
| `delete_first` | O(1) | |
| `delete_last` | O(n) | |
| `delete_node(nodo)` | O(n) | |
| `reverse` | — | |
| `es_palindromo` (tiempo / memoria extra) | — | |
| `intercalar` (listas de n y m elementos) | — | |
| un paso de `for x in l` / de `reversed(l)` | O(1) / no existe | |
| `vaciar` | — | |

| Operación de `BrowserHistory` | Coste |
|-------------------------------|-------|
| `visit` | |
| `back(steps)` | |
| `forward(steps)` | |

¿Por qué el coste de `visit` es *amortizado*? Explícalo con una secuencia concreta de llamadas.

>

## 2 · Medir con el reloj (`comparativa.py`)

Para cada experimento: primero la **predicción** de la razón t(2n)/t(n) de cada columna, después la tabla que te sale (cópiala tal cual) y las respuestas a las preguntas del enunciado.

### A · Vaciar borrando el último

Predicción: `ListaSimple` ≈ ___  `ListaDoble` ≈ ___  `list.pop()` ≈ ___

```
(pega aquí la tabla)
```

>

### B · Borrar nodos de los que ya tenemos la referencia

Predicción: `ListaSimple` ≈ ___  `ListaDoble` ≈ ___  `list.remove(x)` ≈ ___

```
```

>

### C · Recorrer hacia atrás

Predicción: `ListaSimple, l[i]` ≈ ___  `reversed(ListaDoble)` ≈ ___  `reversed(list)` ≈ ___

```
```

>

### D · Memoria por elemento

```
```

¿Cuántos bytes cuesta el puntero `anterior` en cada nodo? ¿Qué porcentaje más ocupa la lista doble que la simple? ¿Y que una `list`?

>

### E · Nodos descartados y recolector de ciclos

```
```

¿Por qué tras `del lista` siguen vivos todos los nodos? ¿Qué hace distinto `vaciar()`? ¿Qué sale en la última fila con tu `visit()`, y qué saldría si solo cortaras `actual.siguiente`?

>

## 3 · Cierre

**1.** Pagar memoria para ganar velocidad: con tus números de A, B y D, ¿compensa el puntero `anterior`? ¿En qué tipo de programa no compensaría?

>

**2.** El historial podría hacerse con una `list` y un índice entero. ¿Qué operación sería igual de buena? ¿Cuál cambiaría? ¿Por qué entonces se usa una lista doble para el LRU Cache que veremos con las tablas hash?

>

**3.** ¿Qué parte de la versión C++ de esta práctica (destructor, constructor de copia, contador de nodos vivos) tiene equivalente en Python, y cuál desaparece? ¿Por qué?

>
