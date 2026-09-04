import os
import urllib.request
import urllib.parse
import json
import time

BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

print("--- JARVIS BOT (SHORTCUT-MODUS) GESTARTET ---")

def send_message(text, target_chat_id):
    if not BOT_TOKEN or not target_chat_id:
        return
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = urllib.parse.urlencode({
        "chat_id": target_chat_id, 
        "text": text,
        "parse_mode": "Markdown",
        "disable_web_page_preview": "false"
    }).encode("utf-8")
    try:
        req = urllib.request.Request(url, data=data)
        with urllib.request.urlopen(req, timeout=10) as response:
            pass
    except Exception as e:
        print("Fehler beim Senden:", e)

def main_loop():
    offset = 0
    print("Jarvis lauscht aktiv auf Telegram...")

    while True:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates?offset={offset}&timeout=30"
        try:
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req, timeout=35) as response:
                ergebnis = json.loads(response.read().decode("utf-8"))

                for update in ergebnis.get("result", []):
                    offset = update["update_id"] + 1
                    if "message" in update and "text" in update["message"]:
                        text = update["message"]["text"]
                        sender_id = str(update["message"]["chat"]["id"])
                        sender_name = update["message"]["from"].get("first_name", "Unbekannt")

                        print(f"\n[BEFEHL EMPFANGEN] Von {sender_name}: '{text}'")

                        text_lower = text.lower().strip()

                        # Exakte Telegram-Befehle oder normale Wörter abfangen
                        if text_lower in ["/pizza", "pizza"]:
                            link = "ubereats://feed?category=pizza"
                            antwort = "🍕 *Befehl ausgeführt, Chef!*\nHier ist die Pizza-Auswahl:\n\n[👉 Pizza bei Uber Eats öffnen]" + f"({link})"
                            send_message(antwort, sender_id)

                        elif text_lower in ["/burger", "burger"]:
                            link = "ubereats://feed?category=burger"
                            antwort = "🍔 *Befehl ausgeführt, Chef!*\nHier ist die Burger-Auswahl:\n\n[👉 Burger bei Uber Eats öffnen]" + f"({link})"
                            send_message(antwort, sender_id)

                        elif text_lower in ["/sushi", "sushi"]:
                            link = "ubereats://feed?category=sushi"
                            antwort = "🍣 *Befehl ausgeführt, Chef!*\nHier ist die Sushi-Auswahl:\n\n[👉 Sushi bei Uber Eats öffnen]" + f"({link})"
                            send_message(antwort, sender_id)

                        elif text_lower in ["/doener", "döner", "doener"]:
                            link = "ubereats://search?q=D%C3%B6ner"
                            antwort = "🥙 *Befehl ausgeführt, Chef!*\nHier ist die Döner-Suche:\n\n[👉 Döner bei Uber Eats öffnen]" + f"({link})"
                            send_message(antwort, sender_id)

                        elif text_lower in ["/pasta", "pasta", "nudeln"]:
                            link = "ubereats://feed?category=pasta"
                            antwort = "🍝 *Befehl ausgeführt, Chef!*\nHier ist die Pasta-Auswahl:\n\n[👉 Pasta bei Uber Eats öffnen]" + f"({link})"
                            send_message(antwort, sender_id)

                        elif text_lower in ["/asiatisch", "asiatisch", "china", "chinese"]:
                            link = "ubereats://feed?category=asian"
                            antwort = "🥡 *Befehl ausgeführt, Chef!*\nHier ist die asiatische Auswahl:\n\n[👉 Asiatisch bei Uber Eats öffnen]" + f"({link})"
                            send_message(antwort, sender_id)

                        elif text_lower in ["/tacos", "tacos", "mexikanisch"]:
                            link = "ubereats://feed?category=mexican"
                            antwort = "🌮 *Befehl ausgeführt, Chef!*\nHier ist die mexikanische Auswahl:\n\n[👉 Tacos & Co. bei Uber Eats öffnen]" + f"({link})"
                            send_message(antwort, sender_id)

                        elif text_lower in ["/chicken", "hähnchen", "chicken"]:
                            link = "ubereats://feed?category=chicken"
                            antwort = "🍗 *Befehl ausgeführt, Chef!*\nHier ist die Hähnchen-Auswahl:\n\n[👉 Hähnchen bei Uber Eats öffnen]" + f"({link})"
                            send_message(antwort, sender_id)

                        elif text_lower in ["/salat", "salat", "gesund"]:
                            link = "ubereats://feed?category=salad"
                            antwort = "🥗 *Befehl ausgeführt, Chef!*\nHier ist die gesunde Auswahl:\n\n[👉 Salate bei Uber Eats öffnen]" + f"({link})"
                            send_message(antwort, sender_id)

                        elif text_lower in ["/dessert", "süß", "eis", "dessert"]:
                            link = "ubereats://feed?category=dessert"
                            antwort = "🍨 *Befehl ausgeführt, Chef!*\nHier ist die Dessert-Auswahl:\n\n[👉 Süßes & Eis bei Uber Eats öffnen]" + f"({link})"
                            send_message(antwort, sender_id)

                        else:
                            send_message(
                                "🤖 *Jarvis hat verstanden:* " + f"'{text}'.\n\n"
                                "Du kannst jetzt ganz schnell Slash-Befehle nutzen:\n"
                                "• /pizza 🍕\n• /burger 🍔\n• /sushi 🍣\n• /doener 🥙\n"
                                "• /pasta 🍝\n• /asiatisch 🥡\n• /tacos 🌮\n"
                                "• /chicken 🍗\n• /salat 🥗\n• /dessert 🍨", 
                                sender_id
                            )

        except urllib.error.URLError:
            time.sleep(2)
        except Exception as e:
            print(f"Fehler: {e}")
            time.sleep(5)

if __name__ == "__main__":
    if not BOT_TOKEN:
        print("Fehler: Token fehlt!")
    else:
        main_loop()
