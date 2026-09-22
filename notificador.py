"""
Envía mensajes de Telegram a través del bot que se creo, usando
la API oficial de Telegram para bots.
"""

import requests
from config import TELEGRAM_CHAT_ID, TELEGRAM_TOKEN

URL_BASE = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"

def enviar_mensaje(texto):
    """
    Envía un mensaje de texto a tu chat de Telegram.
 
    parse_mode="Markdown" le dice a Telegram que interprete cosas
    como *negrita* o [texto](link) dentro del mensaje — así podemos
    mandar el link de la oferta como un enlace clicable en vez de
    una URL larga t compleja
    """
    parametros = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": texto,
        "parse_mode": "Markdown",
    }
    respuesta = requests.post(f"{URL_BASE}/sendMessage", data=parametros)
    respuesta.raise_for_status()

    return respuesta.json()

def notificar_oferta(oferta):
    """
    Formatea los datos de UNA oferta como un mensaje legible y lo
    envía. Reutilizamos esta función cada vez que encontramos una
    oferta nueva.
    """
    mensaje = (
        f"**Nueva Oferte de Empleo**\n\n"
        f"*{oferta['titulo']}*\n"
        f"{oferta['empresa']} - {oferta['ubicacion']}\n\n"
        f"[Ver Oferta]({oferta['link']})\n"
        f"_VIA REMOTIVE_" #SE CUMPLE EL REQUISITO DE MENCIONAR LA FUENTE
    )
    enviar_mensaje(mensaje)

if __name__ == "__main__":
    resultado = enviar_mensaje("BOT de alertas de empleo se encuentra conectado")
    print("Mensaje Enviado Correctamente")