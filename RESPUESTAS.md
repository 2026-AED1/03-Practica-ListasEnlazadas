# Práctica 3 · Hoja de respuestas

**Nombre(s):**

## 1 · Costes de tu implementación

Deben coincidir con los `O(?)` que has sustituido en el código.

| Operación | Lista simple (repaso) | Tu `ListaDoble` |
|-----------|-----------------------|-----------------|
| `insert_first` | O(1) | |
| `insert_last` | O(1) (con puntero a cola) | |
| `insert_before(nodo, x)` | O(n) | |
| `insert_after(nodo, x)` | O(1) | |
| `delete_first` | O(1) | |
| `delete_last` | O(n) | |
| `delete_node(nodo)` | O(n) | |
| `es_palindromo` (tiempo / memoria extra) | — | |
| un paso de `for x in l` / de `reversed(l)` | O(1) / no existe | |

| Operación de `BrowserHistory` | Coste |
|-------------------------------|-------|
| `visit` | |
| `back(steps)` | |
| `forward(steps)` | |

## 2 · Preguntas

**1.** ¿Qué puntero hace que `delete_last` pase de O(n) en la lista simple a O(1) en la doble? ¿Cuánto cuesta ese puntero en memoria?

>

**2.** ¿Por qué el coste de `visit` es *amortizado*? Explícalo con una secuencia concreta de llamadas.

>

**3.** El historial podría hacerse con una `list` y un índice entero. ¿Qué operaciones serían igual de buenas? ¿Por qué entonces se usa una lista doble para estructuras como la caché LRU, donde hay que sacar un elemento de en medio y llevarlo al principio?

>
