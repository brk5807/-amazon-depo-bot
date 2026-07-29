
import os

print("🚀 Amazon Depo Bot Başladı")

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

if BOT_TOKEN:
    print("✅ Telegram Token bulundu")
else:
    print("❌ Telegram Token bulunamadı")

if CHAT_ID:
    print("✅ Chat ID bulundu")
else:
    print("❌ Chat ID bulunamadı")
