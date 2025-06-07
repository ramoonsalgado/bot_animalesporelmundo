import os
import feedparser
import requests

TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]
FEED_URL = "https://animalesporelmundo.com/feed"

LAST_POST_FILE = "last_post.txt"

def get_last_post():
    if os.path.exists(LAST_POST_FILE):
        with open(LAST_POST_FILE, "r") as f:
            return f.read().strip()
    return None

def save_last_post(link):
    with open(LAST_POST_FILE, "w") as f:
        f.write(link)

def get_latest_post():
    feed = feedparser.parse(FEED_URL)
    if feed.entries:
        latest_entry = feed.entries[0]
        title = latest_entry.title
        link = latest_entry.link
        print(f"Último post encontrado: {title} ({link})")

        last_post = get_last_post()
        if last_post != link:
            print("Nuevo post detectado. Enviando mensaje.")
            save_last_post(link)
            send_telegram_message(f"📢 <b>Nuevo post:</b> {title}<br>🔗 <a href=\"{link}\">{link}</a>")
        else:
            print("No hay nuevos posts.")
    else:
        print("No se encontraron entradas en el feed.")

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "HTML"  # Cambiado de Markdown a HTML
    }
    response = requests.post(url, json=payload)
    if response.status_code != 200:
        print(f"Error al enviar el mensaje: {response.status_code} - {response.text}")


if __name__ == "__main__":
    get_latest_post()
