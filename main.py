import os
from telethon import TelegramClient, events

# Variáveis de ambiente (Railway)
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")  # ID onde você recebe os alertas

# Inicializa cliente
client = TelegramClient("bot", API_ID, API_HASH).start(bot_token=BOT_TOKEN)

# Lista de palavras-chave e limites de preço
keywords = {
    "TV SAMSUNG QLED": 2300,
    "IPHONE 16": 4200,
}

# Monitora todas as mensagens
@client.on(events.NewMessage)
async def handler(event):
    text = event.message.message.upper()

    # 🔎 Detectar CUPOM
    if "CUPOM" in text:
        await client.send_message(CHAT_ID, f"🎟️ Cupom encontrado!\n\n{text}")
        return

    # 🔎 Verificar itens com preço
    for item, limite in keywords.items():
        if item in text:
            preco = extrair_preco(text)
            if preco and preco <= limite:
                await client.send_message(
                    CHAT_ID,
                    f"🔥 Promoção encontrada: {item}\nPreço: R$ {preco}\n\n{text}",
                )

# Função auxiliar para extrair preço do texto
def extrair_preco(texto: str):
    import re
    match = re.search(r"(\d{1,3}(?:\.\d{3})*,\d{2})", texto)
    if match:
        valor = match.group(1).replace(".", "").replace(",", ".")
        return float(valor)
    return None

print("🤖 Bot monitorando promoções e cupons...")
client.run_until_disconnected()
