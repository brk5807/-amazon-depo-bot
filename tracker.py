import os
import requests
from bs4 import BeautifulSoup

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

URL = "https://www.amazon.com.tr/s?i=electronics&srs=44219324031&bbn=44219324031&rh=n%3A12466496031%2Cn%3A44219324031%2Cn%3A13709879031"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(URL, headers=headers, timeout=30)
soup = BeautifulSoup(response.text, "html.parser")

products = soup.select("h2 a")

if not products:
    text = "❌ Amazon sayfasında ürün bulunamadı."
else:
    text = "🖥️ Amazon Depo Bilgisayar Bileşenleri\n\n"

    for p in products[:10]:
        name = p.get_text(strip=True)
        link = "https://www.amazon.com.tr" + p["href"]
        text += f"• {name}\n{link}\n\n"

requests.post(
    f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
    json={
        "chat_id": CHAT_ID,
        "text": text[:4000]
    },
    timeout=30
)
