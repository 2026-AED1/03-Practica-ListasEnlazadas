# generar_envio.py  (version C++)
# El juez solo admite UN fichero por envio, y tu codigo esta repartido en
# varios (.hpp + main). Este script copia el contenido de cada
# #include "..." propio dentro del main y genera:
#   envio_lista.cpp       -> problema "Lista doble"
#   envio_historial.cpp   -> problema "Historial de navegador"
#
#   python3 generar_envio.py
#   g++ -std=c++17 -O2 envio_historial.cpp -o envio && ./envio < ../python/ejemplo_historial.txt
#
# No hay que modificarlo. Vuelve a ejecutarlo cada vez que cambies tu codigo.

import os
import re

AQUI = os.path.dirname(os.path.abspath(__file__))
INCLUDE = re.compile(r'^\s*#include\s+"([^"]+)"\s*$')


def expandir(nombre, ya_incluidos):
    lineas = []
    with open(os.path.join(AQUI, nombre), encoding="utf-8") as f:
        for linea in f.read().split("\n"):
            m = INCLUDE.match(linea)
            if m:
                cabecera = m.group(1)
                if cabecera not in ya_incluidos:
                    ya_incluidos.add(cabecera)
                    lineas.append(f"// ===== {cabecera} =====")
                    lineas += expandir(cabecera, ya_incluidos)
                    lineas.append(f"// ===== fin de {cabecera} =====")
            elif linea.strip() == "#pragma once":
                continue
            else:
                lineas.append(linea)
    return lineas


for main, destino in [("main_lista.cpp", "envio_lista.cpp"),
                      ("main_historial.cpp", "envio_historial.cpp")]:
    codigo = ["// " + destino + " -- GENERADO por generar_envio.py a partir de " + main + ".",
              "// No lo edites a mano: cambia tus .hpp y vuelve a generarlo.", ""]
    codigo += expandir(main, set())
    with open(os.path.join(AQUI, destino), "w", encoding="utf-8") as f:
        f.write("\n".join(codigo))
    print("Generado", destino)
