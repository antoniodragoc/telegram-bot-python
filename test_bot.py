import os
import requests

# Leia variáveis de ambiente (igual no Railway)
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def send_test_message():
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": "✅ Teste: seu bot está funcionando! top"
    }
    response = requests.post(url, data=payload)
    print("Status:", response.status_code)
    print("Resposta:", response.json())

if __name__ == "__main__":
    if not BOT_TOKEN or not CHAT_ID:
        print("❌ BOT_TOKEN ou CHAT_ID não configurados!")
    else:
        send_test_message()
