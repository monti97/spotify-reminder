"""
Spotify Reminder Bot
Invia ogni 3 del mese un messaggio Telegram al gruppo,
indicando a chi tocca pagare Spotify questo mese.
"""

import os
import re
import asyncio
from datetime import datetime

import telegram


# ──────────────────────────────────────────────
# CONFIGURA QUI la lista dei nomi partecipanti
# ──────────────────────────────────────────────
NOMI = [
    "Mario",
    "Luigi",
    "Peach",
    "Toad",
    "Yoshi",
    "Wario",
]
# ──────────────────────────────────────────────


def escape_markdownv2(text: str) -> str:
    """
    Esegue l'escape di tutti i caratteri speciali MarkdownV2 di Telegram.
    Ref: https://core.telegram.org/bots/api#markdownv2-style
    """
    special_chars = r"\_*[]()~`>#+-=|{}.!"
    return re.sub(r"([" + re.escape(special_chars) + r"])", r"\\\1", text)


def get_nome_del_mese() -> str:
    """
    Restituisce il nome che tocca questo mese,
    ruotando ciclicamente sull'array NOMI.
    Gennaio (1) → NOMI[0], Febbraio (2) → NOMI[1], …
    e poi riparte da capo ogni volta che si esaurisce la lista.
    """
    mese_corrente = datetime.now().month  # 1–12
    indice = (mese_corrente - 1) % len(NOMI)
    return NOMI[indice]


def build_message(nome: str) -> str:
    """
    Costruisce il messaggio in formato MarkdownV2.
    Il nome viene messo come spoiler (||…||) e in grassetto (*…*).
    I caratteri speciali nel nome vengono escapati correttamente.
    """
    nome_escaped = escape_markdownv2(nome)

    messaggio = (
        "Ehi\\! È arrivato il momento di sganciare\\!\n"
        "Altrimenti Spotify stacca la spina\\!\n"
        f"E questo mese tocca a… ||*{nome_escaped}*||\\!\n"
        "Congratulazioni\\! 🎊 🥳 🎊"
    )
    return messaggio


async def invia_messaggio():
    """
    Legge le variabili d'ambiente, costruisce il messaggio
    e lo invia al gruppo Telegram.
    """
    # Lettura variabili d'ambiente
    token = os.environ.get("TELEGRAM_TOKEN")
    chat_id = os.environ.get("CHAT_ID")

    if not token:
        print("❌ ERRORE: variabile d'ambiente TELEGRAM_TOKEN non impostata.")
        raise SystemExit(1)

    if not chat_id:
        print("❌ ERRORE: variabile d'ambiente CHAT_ID non impostata.")
        raise SystemExit(1)

    # Determina nome e costruisce messaggio
    nome = get_nome_del_mese()
    messaggio = build_message(nome)

    mese_corrente = datetime.now().month
    indice = (mese_corrente - 1) % len(NOMI)
    print(f"📅 Mese: {mese_corrente} | Indice: {indice} | Nome selezionato: {nome}")
    print(f"📨 Testo del messaggio (raw):\n{messaggio}\n")

    # Invio tramite bot Telegram
    try:
        bot = telegram.Bot(token=token)
        await bot.send_message(
            chat_id=chat_id,
            text=messaggio,
            parse_mode=telegram.constants.ParseMode.MARKDOWN_V2,
        )
        print(f"✅ Messaggio inviato con successo al gruppo {chat_id}!")

    except telegram.error.TelegramError as e:
        print(f"❌ Errore Telegram durante l'invio: {e}")
        raise SystemExit(1)


if __name__ == "__main__":
    asyncio.run(invia_messaggio())
