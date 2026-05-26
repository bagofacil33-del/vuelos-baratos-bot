from fast_flights import create_query, get_flights, FlightQuery, Passengers
import asyncio
import telegram
from datetime import datetime, timedelta

# ================== CONFIGURACIÓN ==================
TELEGRAM_TOKEN = "8957881586:AAHOFcVSgQHPh5v16_M_Mv3Gra4umMVk1K0"
CHAT_ID = 8082634911

# Umbrales agresivos
umbrales = {
    "MAD": 950000, "BCN": 950000, "FCO": 950000, "MXP": 950000,
    "LIS": 950000, "AMS": 950000,
    "MEX": 780000, "CUN": 780000, "PUJ": 780000,
    "AUA": 680000, "PTY": 680000, "GYE": 680000,
    "GIG": 520000, "FLN": 520000,
    "ADZ": 520000, "SMR": 520000,
    "SCL": 520000
}

rutas = [
    ("EZE", "MAD"), ("EZE", "BCN"), ("EZE", "FCO"), ("EZE", "MXP"),
    ("EZE", "LIS"), ("EZE", "AMS"),
    ("EZE", "GIG"), ("EZE", "FLN"),
    ("EZE", "ADZ"), ("EZE", "SMR"),
    ("EZE", "AUA"),
    ("EZE", "MEX"), ("EZE", "CUN"),
    ("EZE", "PUJ"), ("EZE", "PTY"), ("EZE", "GYE"), ("EZE", "SCL")
]

async def main():
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    print("🔍 Buscando ofertas imperdibles...")

    for origen, destino in rutas:
        fecha_ida = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
        fecha_vuelta = (datetime.now() + timedelta(days=50)).strftime("%Y-%m-%d")

        try:
            query = create_query(
                flights=[
                    FlightQuery(date=fecha_ida, from_airport=origen, to_airport=destino),
                    FlightQuery(date=fecha_vuelta, from_airport=destino, to_airport=origen)
                ],
                trip="round-trip",
                seat="economy",
                passengers=Passengers(adults=1),
            )

            flights = get_flights(query)
            
            for flight in flights[:3]:
                precio = getattr(flight, 'price', None)
                if precio and precio < umbrales.get(destino, 950000):
                    mensaje = f"""🚨 **OFERTA IMPERDIBLE**

{origen} → {destino} (ida y vuelta)
💰 **${precio:,}**
⏱ {getattr(flight, 'duration', 'N/A')} | {getattr(flight, 'stops', 'N/A')} escalas

🔗 Ver oferta"""

                    await bot.send_message(chat_id=CHAT_ID, text=mensaje, parse_mode='Markdown')
                    print(f"✅ Alerta: {origen}-{destino} ${precio}")
        except Exception as e:
            print(f"Error en {origen}-{destino}: {type(e).__name__} - {e}")

asyncio.run(main())
