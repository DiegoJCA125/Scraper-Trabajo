"""
api_client.py
---------------
Cliente para la API pública y gratuita de Remotive
(https://remotive.com/api/remote-jobs).
 
Reglas que debemos respetar (términos de servicio de Remotive):
- No pedir datos más de ~4 veces al día (sus datos no cambian tan rápido)
- Siempre mostrar el link de vuelta a la oferta en remotive.com
"""

import requests

URL_BASE = "https://remotive.com/api/remote-jobs"

def buscar_ofertas(palabra_clave, limite=20):
    """
    Busca ofertas remotas que contengan la palabra clave
    """
    parametros = {
        "search": palabra_clave,
        "limit": limite,
    }
    respuesta = requests.get(URL_BASE, params=parametros, timeout=10)
    respuesta.raise_for_status() #LANZA ERROR SI LA PETICION FALLA

    datos = respuesta.json()
    ofertas_crudas = datos.get("jobs", [])
    # Nos quedamos solo con los campos que nos interesan, con
    # nombres en español para que el resto de nuestro código sea
    # consistente con la Billetera y el Pomodoro.
    ofertas = []
    for oferta in ofertas_crudas:
        ofertas.append({
            "id": oferta["id"],
            "titulo": oferta["title"],
            "empresa": oferta["company_name"],
            "ubicacion": oferta.get("candidate_required_location", "No especificada"),
            "categoria": oferta.get("category", ""),
            "link": oferta["url"],
        })

    return ofertas
def es_ubicacion_valida(ubicacion):
    """
    Revisa si el texto de ubicación de una oferta sugiere que
    alguien en Colombia puede aplicar.
 
    Remotive no tiene un filtro de país como tal en su API, así que
    lo hacemos nosotros: buscamos palabras clave típicas dentro del
    texto libre que escribe cada empresa (ej. "Worldwide", "LATAM").
 
    .lower() convierte todo a minúsculas antes de comparar, así
    "Worldwide", "WORLDWIDE" y "worldwide" se detectan igual — sin
    esto, una simple diferencia de mayúsculas haría que se nos
    escapen ofertas válidas.
    """
    ubicacion = ubicacion.lower()

    palabras_validas = [
        "worldwide", "latam", "latin america", "colombia",
        "americas", "anywhere", "global",
    ]
    # any(...) devuelve True si AL MENOS UNA de las condiciones
    # dentro es True — no hace falta que las cumpla todas.
    return any(palabra in ubicacion for palabra in palabras_validas)

def buscar_ofertas_filtradas(palabra_clave, limite=20):
    todas = buscar_ofertas(palabra_clave, limite=limite)
    # Una "list comprehension": una forma compacta de escribir un
    # bucle for que construye una lista nueva. Esta línea es
    # equivalente a:
    #   filtradas = []
    #   for oferta in todas:
    #       if es_ubicacion_valida(oferta["ubicacion"]):
    #           filtradas.append(oferta)
    filtradas = [o for o in todas if es_ubicacion_valida(o["ubicacion"])]
    return filtradas

if __name__ == "__main__":
    resultados = buscar_ofertas_filtradas("python", limite=20)
    print(f"Se encontraron {len(resultados)} ofertas donde puedes aplicar desde Colombia:\n")
    for oferta in resultados:
        print(f" - {oferta['titulo']} | {oferta['empresa']} | {oferta['ubicacion']}")
        print(f" {oferta['link']}\n")