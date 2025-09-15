import os
import re
from telethon import TelegramClient, events
import requests

# Variáveis de ambiente (configure no Railway)
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")  # seu ID pessoal para receber alertas
GRUPO = "promo_imperdivel"  # grupo público do Telegram

# Cliente Telethon (usuário normal)
client = TelegramClient("sessao", API_ID, API_HASH)

# Função para enviar mensagem para você via Bot API
def notificar_usuario(texto):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": texto}
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print("Erro ao enviar notificação:", e)

# Evento: quando chegar mensagem nova no grupo
@client.on(events.NewMessage(chats=GRUPO))
async def handler(event):
    texto = event.raw_text.lower()

    if "cervejeira" in texto:
        # extrair números (preços)
        numeros = re.findall(r"\d+", texto.replace(".", "").replace(",", ""))
        for n in numeros:
            preco = int(n)
            if preco < 160000:  # ajustado para lidar com valores tipo 1.599,00 -> 159900
                alerta = f"🔔 Promoção encontrada!\n\n{event.raw_text}"
                print(alerta)
                notificar_usuario(alerta)
                break

print("🤖 Bot rodando... escutando grupo de promoções.")
client.start()
client.run_until_disconnected()
