import os
import requests
from bs4 import BeautifulSoup

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

URL = "https://www.amazon.com.tr/s?i=electronics&srs=44219324031&bbn=44219324031&rh=n%3A12466496031%2Cn%3A44219324031%2Cn%3A13709879031"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0 Safari/537.36",
    "Accept-Language": "tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7"
}

try:
    response = requests.get(URL, headers=headers, timeout=20)

    print("HTTP Durumu:", response.status_code)

    soup = BeautifulSoup(response.text, "html.parser")

    products = soup.select("div[data-component-type='s-search-result']")

    print("Bulunan ürün sayısı:", len(products))

    if not products:
        text = "❌ Amazon sayfasında ürün bulunamadı.\n\nMuhtemelen Amazon GitHub IP'sine CAPTCHA gösteriyor."
    else:
        text = "🖥 Amazon Türkiye Depo Ürünleri\n\n"

        for item in products[:10]:
            a = item.select_one("h2 a")
            if not a:
                continue

            name = a.get_text(strip=True)

            href = a.get("href", "")
            if href.startswith("/"):
                href = "https://www.amazon.com.tr" + href

            text += f"• {name}\n{href}\n\n"

except Exception as e:
    text = f"❌ Hata:\n{e}"

requests.post(
    f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
    json={
        "chat_id": CHAT_ID,
        "text": text
    },
    timeout=20
)
