from flask import Flask, request
import requests
import os

app = Flask(__name__)

VERIFY_TOKEN = "panda_barber_verify"

ACCESS_TOKEN = os.getenv("WHATSAPP_TOKEN")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")

WHATSAPP_API_URL = f"https://graph.facebook.com/v18.0/{PHONE_NUMBER_ID}/messages"


def enviar_mensaje(numero, texto):
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "messaging_product": "whatsapp",
        "to": numero,
        "text": {"body": texto}
    }

    response = requests.post(WHATSAPP_API_URL, headers=headers, json=payload)
    print("STATUS:", response.status_code)
    print("RESPUESTA:", response.text)


@app.route("/")
def home():
    return "Panda Barber Bot activo 🐼✂️"


@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        mode = request.args.get("hub.mode")
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")

        if mode == "subscribe" and token == VERIFY_TOKEN:
            return challenge, 200
        return "Error", 403

        data = request.json
    print("DATA COMPLETA:", data)

    try:
        entry = data["entry"][0]
        changes = entry["changes"][0]
        value = changes["value"]

        if "messages" not in value:
            print("No hay mensajes en el payload")
            return "EVENT_RECEIVED", 200

        mensaje = value["messages"][0]
        numero = mensaje["from"]

        if "text" not in mensaje:
            enviar_mensaje(
                numero,
                "🐼✂️ Panda Barber\n\n"
                "Por favor envíame un mensaje de texto 😊\n"
                "Escribe *hola* para comenzar."
            )
            return "EVENT_RECEIVED", 200

        texto = mensaje["text"]["body"].strip().lower()
        print(f"Mensaje de {numero}: {texto}")

        if texto in ["hola", "buenas", "hey", "hello"]:
            enviar_mensaje(
                numero,
                "🐼✂️ *Panda Barber*\n\n"
                "¡Hey! 😎 Bienvenido.\n\n"
                "1️⃣ Ver servicios y precios\n"
                "2️⃣ Ver horarios y ubicación\n"
                "3️⃣ Agendar un turno\n"
                "4️⃣ Cancelar un turno\n\n"
                "Responde con el número 👇"
            )

        elif texto == "1":
            enviar_mensaje(
                numero,
                "✂️ *Servicios y precios*\n\n"
                "• Corte clásico — $8\n"
                "• Fade — $10\n"
                "• Barba — $5\n"
                "• Corte + barba — $13"
            )

        elif texto == "2":
            enviar_mensaje(
                numero,
                "📍 *Horarios y ubicación*\n\n"
                "🕒 Lunes a Sábado: 10am – 8pm\n"
                "📍 Centro de la ciudad"
            )

        elif texto == "3":
            enviar_mensaje(
                numero,
                "📅 *Agendar turno*\n\n"
                "Dime fecha, hora y servicio.\n"
                "Ejemplo: mañana 5pm, fade"
            )

        elif texto == "4":
            enviar_mensaje(
                numero,
                "❌ *Cancelar turno*\n\n"
                "Dime la fecha y hora del turno."
            )

        else:
            enviar_mensaje(
                numero,
                "🤔 No entendí.\nEscribe *hola* para el menú."
            )

    except Exception as e:
        print("ERROR GRAVE EN WEBHOOK:", e)


    return "EVENT_RECEIVED", 200
