"""
Conecta las 3 piezas que ya se construyeron por separado:
 
1. api_client.py  -> busca ofertas en Remotive
2. historial.py   -> filtra cuáles son nuevas (no notificadas antes)
3. notificador.py -> envía las nuevas por Telegram
 
Ejecutar este único archivo hace todo el proceso de punta a punta.
"""
from api_client import buscar_ofertas_filtradas
from historial import filtrar_ofertas_nuevas
from notificador import notificar_oferta

# agregar más palabras aquí — el script buscará cada una por
# separado y avisará de las ofertas nuevas de todas ellas.
PALABRAS_CLAVE = ["python", "sql"]

def ejecutar_busqueda():
    """
    Recorre cada palabra clave, busca ofertas, filtra las nuevas,
    y notifica cada una por Telegram.
    """
    total_notificadas = 0

    for palabra in PALABRAS_CLAVE:
        print(f"\n Buscando ofertas para: {palabra}")
        ofertas = buscar_ofertas_filtradas(palabra, limite=20)
        ofertas_nuevas = filtrar_ofertas_nuevas(ofertas)

        print(f"    {len(ofertas)} encontradas, {len(ofertas_nuevas)} nuevas")

        for oferta in ofertas_nuevas:
            notificar_oferta(oferta)
            print(f" NOTIFICADO: {oferta['titulo']}")
            total_notificadas += 1

    if total_notificadas == 0:
        print("\n No habia ofertas nuevas esta vez")
    else:
        print(f"\n Se notifican {total_notificadas} ofertas nuevas en total")

if __name__ == "__main__":
    ejecutar_busqueda()