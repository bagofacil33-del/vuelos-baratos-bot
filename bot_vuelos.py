from fast_flights import FlightQuery, Passengers, get_flights
import asyncio
import telegram
from datetime import datetime, timedelta

# ================== CONFIGURACIÓN ==================
TELEGRAM_TOKEN = "8957881586:AAHOFcVSgQHPh5v16_M_Mv3Gra4umMVk1K0"
CHAT_ID = 8082634911

# Umbrales basados en históricos (agresivos)
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
            # Nueva forma de usar la librería
            query = get_flights(
                origin=origen,
                destination=destino,
                departure_date=fecha_ida,
                return_date=fecha_vuelta,
                trip_type="round_trip",
                travelers=Passengers(adults=1),
                max_stops=2
            )
            
            flights = query[:5]  # Tomamos los primeros resultados
            
            for flight in flights:
                precio = getattr(flight, 'price', None)
                if precio and precio < umbrales.get(destino, 950000):
                    mensaje = f"""🚨 **OFERTA IMPERDIBLE**

{origen} → {destino} (ida y vuelta)
💰 **${precio:,}**
⏱ {getattr(flight, 'duration', 'N/A')} | {getattr(flight, 'stops', 'N/A')} escalas

🔗 Ver en Google Flights"""
                    
                    await bot.send_message(chat_id=CHAT_ID, text=mensaje, parse_mode='Markdown')
                    print(f"✅ Alerta enviada: {origen}-{destino} ${precio}")
        except Exception as e:
            print(f"Error en {origen}-{destino}: {e}")

asyncio.run(main())
