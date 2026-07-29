import requests
from bs4 import BeautifulSoup
import os

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

URL = "https://www.amazon.com.tr/s?i=electronics&srs=44219324031&bbn=44219324031&rh=n%3A12466496031%2Cn%3A44219324031%2Cn%3A13709879031"

headers = {
    "User-Agent": "Mozilla/5.0"
}

def send_message(text):
    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        json={
            "chat_id": CHAT_ID,
            "text": text
        },
        timeout=20
    )

try:
    r = requests.get(URL, headers=headers, timeout=20)
    soup = BeautifulSoup(r.text, "lxml")

    products = soup.select("[data-component-type='s-search-result']")

    send_message(
        f"✅ Amazon sayfasına bağlanıldı.\n📦 Bulunan ürün sayısı: {len(products)}"
    )

except Exception as e:
    send_message(f"❌ Hata oluştu:\n{e}")
