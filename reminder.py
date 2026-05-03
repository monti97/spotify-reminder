"""
Spotify Reminder Bot
"""

import os
import re
import asyncio
from datetime import datetime

import telegram

# Nomi fissi (posizioni 1-5)
NOMI_FISSI = [
    "Stefano",
    "Chiara",
    "Wash",
    "Belloandre",
    "Daniele",
]

# Anno di partenza del ciclo (giugno 2026 = prima occorrenza)
ANNO_INIZIO = 2026

# File con i nomi variabili per il 6° posto
FILE_NOMI_VARIABILI = "nomi_variabili.txt"


def carica_nomi_variabili() -> list:
    try:
        with open(FILE_NOMI_VARIABILI, "r", encoding="utf-8") as f:
            nomi = [riga.strip() for riga in f if riga.strip()]
        if nomi:
            return nomi
    except FileNotFoundError:
        pass
    return ["Drago"]


def get_occorrenza_sesto_posto() -> int:
    """
    Conta quante volte è toccato il 6° posto (giugno e dicembre)
    dall'anno di inizio fino ad oggi incluso.
    Giugno 2026 = 0, Dicembre 2026 = 1, Giugno 2027 = 2, ecc.
    """
    ora = datetime.now()
    anno = ora.year
    mese = ora.month

    # Ogni anno ha 2 occorrenze (giugno e dicembre)
    anni_passati = anno - ANNO_INIZIO
    occorrenze = anni_passati * 2

    # Se siamo a dicembre aggiungiamo anche la seconda occorrenza dell'anno
    if mese == 12:
        occorrenze += 1

    return occorrenze


def escape_markdownv2(text: str) -> str:
    special_chars = r"\_*[]()~`>#+-=|{}.!"
    return re.sub(r"([" + re.escape(special_chars) + r"])", r"\\\1", text)


def get_nome_del_mese() -> str:
    mese = datetime.now().month
    indice_fisso = (mese - 1) % 6  # 0-4 = nomi fissi, 5 = sesto posto

    if indice_fisso < 5:
        return NOMI_FISSI[
