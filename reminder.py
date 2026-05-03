import os
import re
import asyncio
from datetime import datetime
import telegram

NOMI_FISSI = [
    "Stefano",
    "Chiara",
    "Wash",
    "Belloandre",
    "Daniele",
]

ANNO_INIZIO = 2026
FILE_NOMI_VARIABILI = "nomi_variabili.txt"


def carica_nomi_variabili():
    try:
        with open(FILE_NOMI_VARIABILI, "r", encoding="utf-8") as f:
            nomi = [riga.strip() for riga in f if riga.strip()]
        if nomi:
            return nomi
    except FileNotFoundError:
        pass
    return ["Drago"]


def get_occorrenza_sesto_posto():
    ora = datetime.now()
    anni_passati = ora.year - ANNO_INIZIO
    occorrenze = anni_passati * 2
    if ora.month == 12:
        occorrenze += 1
    return occorrenze


def escape_markdownv2(text):
    special_chars = r"\_*[]()~`>#+-=|{}.!"
    return re.sub(r"([" + re.escape(special_chars) + r"])", r"\\\1", text)


def get_nome_del_mese():
    mese = datetime.now().month
    indice_fisso = (mese - 4) % 6
    if indice_fisso < 5:
        return NOMI_FISSI[indice_fisso]
    else:
        nomi_variabili = carica_nomi_variabili()
        occorrenza = get_occorrenza_sesto_posto()
        indice_variabile = occorrenza % len(nomi_variabili)
        return nomi_variabili[indice_variabile]


def build_message(nome):
    nome_escaped = escape_markdownv2(nome)
    return (
        "Ehi\\! È arrivato il momento di sganciare\\!\n"
        "Altrimenti Spotify stacca la spina\\!\n"
        f"E questo mese tocca a… ||*{nome_escaped}*||\\!\n"
        "Congratulazioni\\! 🎊 🥳 🎊"
    )


async def invia_messaggio():
    token = os.environ.get("TELEGRAM_TOKEN")
    chat_id = os.environ.get("CHAT_ID")

    if not token:
        print("❌ ERRORE: variabile d'ambiente TELEGRAM_TOKEN non impostata.")
        raise SystemExit(1)
    if not chat_id:
        print("❌ ERRORE: variabile d'ambiente CHAT_ID non impostata.")
        raise SystemExit(1)

    nome = get_nome_del_mese()
    messaggio = build_message(nome)
    print(f"📅 Mese: {datetime.now().month} | Nome: {nome}")

    try:
        bot = telegram.Bot(token=token)
        await bot.send_message(
            chat_id=chat_id,
            text=messaggio,
            parse_mode=telegram.constants.ParseMode.MARKDOWN_V2,
        )
        print(f"✅ Messaggio inviato con successo al gruppo {chat_id}!")
    except telegram.error.TelegramError as e:
        print(f"❌ Errore Telegram: {e}")
        raise SystemExit(1)


if __name__ == "__main__":
    asyncio.run(invia_messaggio())
