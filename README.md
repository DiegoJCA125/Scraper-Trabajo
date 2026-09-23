# 🔔 Alertas de Empleo

Automatización en Python que busca ofertas de empleo remoto según palabras clave, filtra las que aceptan candidatos desde Colombia, y notifica las ofertas nuevas directamente a Telegram — sin repetir notificaciones de ofertas ya vistas.

## ✨ Funcionalidades

- Búsqueda de ofertas por palabra clave usando la API pública de [Remotive](https://remotive.com)
- Filtro automático de ubicación (solo ofertas donde alguien en Colombia puede aplicar: Worldwide, LATAM, etc.)
- Deduplicación: nunca notifica dos veces la misma oferta
- Notificaciones instantáneas por Telegram, con título, empresa, ubicación y link directo
- Manejo seguro de credenciales (Token y Chat ID nunca se suben al repositorio)

## 🛠️ Stack técnico

| Capa | Tecnología |
|---|---|
| Backend | Python |
| Fuente de datos | API pública de Remotive |
| Notificaciones | API de Bots de Telegram |
| Persistencia | Archivo JSON local (historial de ofertas vistas) |
| Control de versiones | Git / GitHub |

## 🏗️ Arquitectura

```
main.py (orquestador)
   │
   ├── api_client.py   → busca ofertas en Remotive + filtra ubicación
   ├── historial.py    → descarta ofertas ya notificadas antes
   └── notificador.py  → envía las ofertas nuevas por Telegram
```

Cada módulo tiene una sola responsabilidad, siguiendo el mismo principio de diseño que mi otro proyecto, [Billetera Personal](https://github.com/DiegoJCA125/Billetera-Personal).

## 🧭 Decisiones técnicas (y por qué)

- **¿Por qué Remotive y no scraping de Indeed/LinkedIn/Computrabajo?** Lo intenté primero con scraping directo de Indeed, pero su protección anti-bot (Cloudflare) bloqueó las peticiones con error 403. Insistir contra eso implica un juego constante de gato y ratón, y roza los términos de servicio del sitio. Remotive ofrece una API pública, gratuita y estable — una solución mucho más robusta y honesta.
- **¿Por qué Telegram y no WhatsApp?** Inicialmente probé con CallMeBot (un servicio no oficial para WhatsApp), pero resultó poco confiable. La API de Bots de Telegram es oficial, gratuita, y se configura en minutos.

## 🚀 Cómo correrlo localmente

1. Clona el repositorio e instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```
2. Crea un bot de Telegram hablando con [@BotFather](https://t.me/BotFather) y obtén tu Token.
3. Obtén tu Chat ID enviándole un mensaje a tu bot y consultando `https://api.telegram.org/bot<TU_TOKEN>/getUpdates`.
4. Crea un archivo `config.py` en la raíz del proyecto:
   ```python
   TELEGRAM_TOKEN = "tu_token_aqui"
   TELEGRAM_CHAT_ID = "tu_chat_id_aqui"
   ```
5. Ajusta las palabras clave de búsqueda en `main.py` (`PALABRAS_CLAVE`).
6. Corre el script:
   ```bash
   python main.py
   ```

## 📚 Qué aprendí construyendo esto

- Los límites reales del web scraping: no todos los sitios lo permiten, y hay que tener un plan B
- Consumo de APIs REST públicas y manejo de JSON
- Automatización de notificaciones vía bots de Telegram
- Deduplicación de datos usando estructuras `set` de Python
- Diseño modular: separar "buscar", "recordar" y "notificar" en archivos independientes

## 🔮 Posibles mejoras futuras

- Ejecución automática programada (Programador de tareas / cron) - Realizada
- Más fuentes de empleo (revisando su estructura una por una)
- Filtro por salario o tipo de contrato
- Historial consultable en una interfaz web, como en Billetera Personal

---

Proyecto desarrollado como parte de mi ruta de aprendizaje en Data Engineering.