# Chuleta — Lista doblemente enlazada e historial de navegador

```
    cabeza                              cola
      │                                   │
      ▼                                   ▼
┌───┬────┬───┐    ┌───┬────┬───┐    ┌───┬────┬───┐
│   │ A  │ ●─┼───►│   │ B  │ ●─┼───►│   │ C  │ × │
│ × │    │   │◄───┼─● │    │   │◄───┼─● │    │   │    tamano = 3
└───┴────┴───┘    └───┴────┴───┘    └───┴────┴───┘
```

## Insertar X al inicio (lista no vacía) — 4 punteros, en este orden
```
1. X.siguiente = cabeza
2. X.anterior  = None
3. cabeza.anterior = X
4. cabeza = X
```
Lista vacía: `cabeza = cola = X`. (Al final es simétrico: cambia `cabeza` por `cola` y `siguiente` por `anterior`.)

## Insertar X detrás de un nodo N (N no es la cola)
```
X.anterior = N
X.siguiente = N.siguiente
N.siguiente.anterior = X
N.siguiente = X
```

## Eliminar un nodo dado (`delete_node`)
```
if nodo.anterior is not None: nodo.anterior.siguiente = nodo.siguiente
else:                         cabeza = nodo.siguiente
if nodo.siguiente is not None: nodo.siguiente.anterior = nodo.anterior
else:                          cola = nodo.anterior
nodo.anterior = nodo.siguiente = None
tamano -= 1
```
Casos especiales: el nodo es la cabeza / es la cola / es el único elemento.

## Invariante (lo comprueba `invariante_correcto()`)
- `tamano == 0` ⇔ `cabeza is None` ⇔ `cola is None`
- `cabeza.anterior is None`, `cola.siguiente is None`
- de `cabeza` a `cola` por `siguiente` hay exactamente `tamano` nodos
- `x.anterior.siguiente is x` para todo nodo que no sea la cabeza

## Palíndromo — dos punteros convergentes
```
inicio, fin = cabeza, cola
repetir tamano // 2 veces:
    si inicio.dato != fin.dato: return False
    inicio, fin = inicio.siguiente, fin.anterior
return True
```

## Python
| Escribes | Python llama a |
|---|---|
| `len(l)` | `l.__len__()` |
| `for x in l` | `l.__iter__()` (un generador con `yield`) |
| `reversed(l)` | `l.__reversed__()` |
| `x in l` | recorre con `__iter__` |
| `print(l)` | `l.__str__()` |

`None` ≈ `nullptr` · compara con `is` · `b = a` no copia: es otro nombre para la misma lista.

## Historial de navegador
Misma `ListaDoble` + un puntero `actual` al nodo de la página en la que estás. Sin tablas hash.

- **visit(url)**: descartar lo que hay detrás de `actual` → enlazar nodo nuevo → `actual` = nuevo
- **back(steps)**: mover `actual` por `.anterior` hasta `steps` veces o hasta el principio
- **forward(steps)**: mover `actual` por `.siguiente` hasta `steps` veces o hasta el final

⚠️ Error nº 1: `visit()` tras `back()` sin descartar bien lo que había por delante.

## Costes
| Operación | Lista simple | Lista doble | Historial |
|---|---|---|---|
| Insertar al inicio | O(1) | O(1) | — |
| Insertar al final | O(1)* | O(1) | — |
| Insertar antes de un nodo dado | O(n) | O(1) | — |
| Eliminar primero | O(1) | O(1) | — |
| Eliminar último | O(n) | O(1) | — |
| Eliminar nodo dado | O(n) | O(1) | — |
| Recorrer hacia atrás | no se puede (O(n²) con índices) | O(n) | — |
| `visit` | — | — | O(1) amortizado |
| `back` / `forward` | — | — | O(min(steps, n)) |

\* solo si la lista simple guarda puntero a `cola`.
