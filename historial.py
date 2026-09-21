"""
historial.py
--------------
Recuerda qué ofertas ya te notificamos antes, guardando sus IDs en
un archivo JSON local (ofertas_vistas.json).

¿Por qué JSON y no una Google Sheet como en la Billetera?
Aquí no necesitamos ver ni editar esta información nosotros mismos
—es solo "memoria interna" del programa—, así que un archivo local
simple es más que suficiente. Reservamos Google Sheets para datos
que SÍ quieres consultar tú directamente.
"""

import json
import os

ARCHIVO_HISTORIAL = "ofertas_vistas.json"


def cargar_ids_vistos():
    """
    Lee el archivo de historial y devuelve un set (conjunto) con
    los IDs de ofertas ya notificadas.

    Un set es como una lista, pero sin duplicados y con búsquedas
    MUCHO más rápidas ("¿está este ID aquí?" es casi instantáneo,
    sin importar cuántos IDs tenga guardados).

    Si el archivo todavía no existe (primera vez que corres esto),
    devolvemos un set vacío en vez de dar error.
    """
    if not os.path.exists(ARCHIVO_HISTORIAL):
        return set()

    with open(ARCHIVO_HISTORIAL, "r") as archivo:
        lista_ids = json.load(archivo)

    return set(lista_ids)


def guardar_ids_vistos(ids_vistos):
    """
    Guarda el set de IDs en el archivo JSON. json.dump() no sabe
    escribir sets directamente, así que lo convertimos a list()
    primero.
    """
    with open(ARCHIVO_HISTORIAL, "w") as archivo:
        json.dump(list(ids_vistos), archivo)


def filtrar_ofertas_nuevas(ofertas):
    """
    Recibe una lista de ofertas (como las que devuelve api_client.py)
    y devuelve solo las que NO hemos notificado todavía.

    También actualiza el archivo de historial, agregando los IDs
    de estas ofertas nuevas — así la próxima vez que corra el
    script, ya no las vuelve a mostrar.
    """
    ids_vistos = cargar_ids_vistos()

    ofertas_nuevas = [o for o in ofertas if o["id"] not in ids_vistos]

    # Agregamos los IDs de las ofertas nuevas al set de vistos.
    # .update() agrega varios elementos a la vez, a diferencia de
    # .add() que agrega uno solo.
    for oferta in ofertas_nuevas:
        ids_vistos.add(oferta["id"])

    guardar_ids_vistos(ids_vistos)

    return ofertas_nuevas


if __name__ == "__main__":
    from api_client import buscar_ofertas_filtradas

    ofertas = buscar_ofertas_filtradas("python", limite=20)
    nuevas = filtrar_ofertas_nuevas(ofertas)

    print(f"De {len(ofertas)} ofertas encontradas, {len(nuevas)} son nuevas:\n")
    for oferta in nuevas:
        print(f"- {oferta['titulo']} | {oferta['empresa']}")