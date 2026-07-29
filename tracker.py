import os
import requests

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

URL = "https://www.amazon.com.tr/s?i=electronics&srs=44219324031&bbn=44219324031&rh=n%3A12466496031%2Cn%3A44219324031%2Cn%3A13709879031"

headers = {
    "User-Agent": "Mozilla/5.0"
}

try:
    response = requests.get(URL, headers=headers, timeout=30)

    text = f"HTTP: {response.status_code}\n\n{response.text[:500]}"

except Exception as e:
    text = f"HATA:\n{e}"

requests.post(
    f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
    json={
        "chat_id": CHAT_ID,
        "text": text
    },
    timeout=30
)
