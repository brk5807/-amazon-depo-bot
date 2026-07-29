from playwright.sync_api import sync_playwright
import requests
import os
import json
import time

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

URL = "https://www.amazon.com.tr/s?i=electronics&srs=44219324031&bbn=44219324031&rh=n%3A12466496031%2Cn%3A44219324031%2Cn%3A13709879031"

KEYWORDS = [
    "rtx",
    "5060",
    "5070",
    "5080",
    "5090",
    "ryzen",
    "7800x3d",
    "9800x3d",
    "7500f",
    "7700",
    "9600x",
    "b650",
    "b850",
    "x870",
    "ssd",
    "nvme",
    "ddr5",
    "ram"
]

STATE_FILE = "seen.json"

if os.path.exists(STATE_FILE):
    with open(STATE_FILE, "r", encoding="utf-8") as f:
        seen = json.load(f)
else:
    seen = []

def send(text):
    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        json={
            "chat_id": CHAT_ID,
            "text": text[:4000]
        },
        timeout=30
    )

with sync_playwright() as p:

    browser = p.chromium.launch(
        headless=True
    )

    page = browser.new_page(
        locale="tr-TR",
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/138.0 Safari/537.36"
    )

    page.goto(URL, wait_until="networkidle", timeout=60000)

    time.sleep(5)

    cards = page.locator("div[data-component-type='s-search-result']")

    count = cards.count()
    send(f"Bulunan ürün sayısı: {count}")
    
    found = []

    for i in range(count):

        card = cards.nth(i)

        try:
            title = card.locator("h2").inner_text().strip()
        except:
            continue

        lower = title.lower()

        ok = False

        for word in KEYWORDS:
            if word in lower:
                ok = True
                break

        if not ok:
            continue
        try:
            href = card.locator("h2 a").get_attribute("href")
        except:
            continue

        if not href:
            continue

        if href.startswith("/"):
            link = "https://www.amazon.com.tr" + href
        else:
            link = href

        if link in seen:
            continue

        found.append((title, link))
        seen.append(link)

    browser.close()

if found:

    msg = "🖥 Amazon Depo Bilgisayar Bileşenleri\n\n"

    for title, link in found[:10]:
        msg += f"• {title}\n{link}\n\n"

    send(msg)

    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(seen, f, ensure_ascii=False, indent=2)

else:
    send("ℹ️ Yeni bilgisayar bileşeni bulunamadı.")