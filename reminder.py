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
    mes
