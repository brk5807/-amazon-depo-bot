import os
import requests
from bs4 import BeautifulSoup

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

URL = "https://www.amazon.com.tr/s?i=electronics&srs=44219324031&bbn=44219324031&rh=n%3A12466496031%2Cn%3A44219324031%2Cn%3A13709879031"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
    "Accept-Language": "tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Referer": "https://www.amazon.com.tr/"
}

try:
    response = requests.get(URL, headers=headers, timeout=30)

    debug = (
        f"HTTP: {response.status_code}\n\n"
        f"{response.text[:3000]}"
    )

    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        json={
            "chat_id": CHAT_ID,
            "text": debug[:4000]
        },
        timeout=30
    )

except Exception as e:
    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        json={
            "chat_id": CHAT_ID,
            "text": f"HATA:\n{e}"
        },
        timeout=30
    )
    # test
