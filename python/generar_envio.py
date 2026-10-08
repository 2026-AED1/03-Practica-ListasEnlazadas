# generar_envio.py
# Junta lista_doble.py e historial.py en UN SOLO fichero, envio_historial.py,
# que es el que se sube al problema "Historial de navegador" del juez.
# (El historial usa tu ListaDoble, asi que el envio necesita las dos clases.)
# Para el problema "Lista doble" se sube lista_doble.py tal cual.
#
#   python3 generar_envio.py
#   python3 envio_historial.py < ejemplo_historial.txt      # pruebalo antes de subirlo
#
# No hay que modificarlo. Vuelve a ejecutarlo cada vez que cambies tu codigo.

import os

AQUI = os.path.dirname(os.path.abspath(__file__))


def leer(nombre):
    with open(os.path.join(AQUI, nombre), encoding="utf-8") as f:
        return f.read()


def sin_demo(codigo):
    # Quita el bloque final  if __name__ == "__main__":  (la demostracion).
    marca = '\nif __name__ == "__main__":'
    i = codigo.rfind(marca)
    return codigo[:i].rstrip() + "\n" if i != -1 else codigo


def sin_import_propio(codigo):
    # En un solo fichero las clases ya estan arriba: sobra el import.
    return "\n".join(l for l in codigo.split("\n")
                     if not l.startswith("from lista_doble import"))


lista = sin_demo(leer("lista_doble.py"))
historial = sin_import_propio(leer("historial.py"))

envio = ("# envio_historial.py -- GENERADO por generar_envio.py. No lo edites a mano:\n"
         "# cambia lista_doble.py / historial.py y vuelve a generarlo.\n\n"
         + lista
         + "\n\n# " + "=" * 70 + "\n# historial.py\n# " + "=" * 70 + "\n\n"
         + historial)

destino = os.path.join(AQUI, "envio_historial.py")
with open(destino, "w", encoding="utf-8") as f:
    f.write(envio)
print(f"Generado {destino}")
print("Pruebalo con:  python3 envio_historial.py < ejemplo_historial.txt")
