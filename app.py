from flask import Flask, request

app = Flask(__name__)

VERIFY_TOKEN = "panda_barber_verify"

@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    # Verificación inicial de Meta
    if request.method == "GET":
        mode = request.args.get("hub.mode")
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")

        if mode == "subscribe" and token == VERIFY_TOKEN:
            return challenge, 200
        else:
            return "Error de verificación", 403

    # Mensajes entrantes
    if request.method == "POST":
        data = request.json

        try:
            mensaje = data["entry"][0]["changes"][0]["value"]["messages"][0]["text"]["body"]
            print("Mensaje recibido:", mensaje)
        except:
            pass

        return "EVENT_RECEIVED", 200


@app.route("/")
def home():
    return "Panda Barber Bot activo 🐼✂️"


if __name__ == "__main__":
    app.run()
