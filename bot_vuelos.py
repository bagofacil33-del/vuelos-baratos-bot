from fast_flights import create_query, get_flights, FlightQuery, Passengers
import asyncio
import telegram
from datetime import datetime, timedelta

# ================== CONFIGURACIÓN ==================
TELEGRAM_TOKEN = "8957881586:AAHOFcVSgQHPh5v16_M_Mv3Gra4umMVk1K0"
CHAT_ID = 8082634911

# Umbrales basados en mínimos históricos + varianza ±100 USD (~±150.000 ARS)
umbrales = {
    # Europa
    "MAD": 950000, "BCN": 950000, "FCO": 950000, "MXP": 950000,
    "LIS": 950000, "AMS": 950000,
    
    # México y Caribe
    "MEX": 780000, "CUN": 780000, "PUJ": 780000,
    
    # Caribe / Sudamérica media
    "AUA": 680000, "PTY": 680000, "GYE": 680000,
    
    # Regionales (los más baratos)
    "GIG": 520000, "FLN": 520000,
    "ADZ": 520000, "SMR": 520000,
    "SCL": 520000
}

rutas = [
    # Europa
    ("EZE", "MAD"), ("EZE", "BCN"),
    ("EZE", "FCO"), ("EZE", "MXP"),
    ("EZE", "LIS"),
    ("EZE", "AMS"),

    # Latinoamérica y Caribe
    ("EZE", "GIG"), ("EZE", "FLN"),     # Brasil
    ("EZE", "ADZ"), ("EZE", "SMR"),     # Colombia
    ("EZE", "AUA"),                     # Aruba
    ("EZE", "MEX"), ("EZE", "CUN"),     # México
    ("EZE", "PUJ"),                     # Punta Cana
    ("EZE", "PTY"),                     # Panamá
    ("EZE", "GYE"),                     # Ecuador
    ("EZE", "SCL")                      # Chile
]

async def main():
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    print("🔍 Buscando ofertas imperdibles (basado en históricos)...")

    for origen, destino in rutas:
        fecha_ida = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
        fecha_vuelta = (datetime.now() + timedelta(days=50)).strftime("%Y-%m-%d")

        query = create_query(
            flights=[
                FlightQuery(date=fecha_ida, from_airport=origen, to_airport=destino),
                FlightQuery(date=fecha_vuelta, from_airport=destino, to_airport=origen)
            ],
            trip="round-trip",
            seat="economy",
            passengers=Passengers(adults=1),
        )

        try:
            flights = get_flights(query)
            for flight in flights[:3]:
                precio = flight.price
                umbral = umbrales.get(destino, 950000)
                
                if precio and precio < umbral:
                    mensaje = f"""🚨 **OFERTA IMPERDIBLE**

{origen} → {destino} (ida y vuelta)
💰 **${precio:,}**
⏱ {flight.duration} | {flight.stops} escalas
📅 {flight.departure_date}

🔗 {flight.url}"""

                    await bot.send_message(chat_id=CHAT_ID, text=mensaje, parse_mode='Markdown')
                    print(f"✅ Alerta: {origen}-{destino} ${precio}")
        except Exception as e:
            print(f"Error en {origen}-{destino}: {e}")

asyncio.run(main())
