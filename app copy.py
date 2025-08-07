
import streamlit as st
import re
import time

def parse_user_input(text):
    filters = {}

    # Lokalizacja
    loc_match = re.search(r"(na|w)\s+([a-ząćęłńóśźż]+)", text.lower())
    if loc_match:
        filters["lokalizacja"] = loc_match.group(2)

    # Liczba pokoi
    pokoje_match = re.search(r"(\d+)\s*(pok|pokoje|pokój)", text.lower())
    if pokoje_match:
        filters["pokoje"] = int(pokoje_match.group(1))

    # Metraż
    metraz_match = re.search(r"(\d+)\s*(m2|m²|metrów|metr|m)", text.lower())
    if metraz_match:
        filters["metraz"] = int(metraz_match.group(1))

    # Balkon
    balkon_keywords = ["balkon", "balkonie", "balkonu", "z balkonem", "balkony"]
    if any(k in text.lower() for k in balkon_keywords):
        filters["balkon"] = True

    # Cena maksymalna
    cena_match = re.search(r"(do|max|maks|cena)\s*(\d+)", text.lower())
    if cena_match:
        filters["cena_max"] = int(cena_match.group(2))

    # Piętro
    pietro_match = re.search(r"(parter|\d+)\s*(pi[eę]tro|pietro)", text.lower())
    if pietro_match:
        if pietro_match.group(1) == "parter":
            filters["pietro"] = 0
        else:
            filters["pietro"] = int(pietro_match.group(1))

    # Typ budynku (prosty przykład)
    if "blok" in text.lower():
        filters["typ_budynku"] = "blok"
    elif "kamienica" in text.lower():
        filters["typ_budynku"] = "kamienica"
    elif "apartamentowiec" in text.lower():
        filters["typ_budynku"] = "apartamentowiec"

    # Garaż / parking
    if any(k in text.lower() for k in ["garaż", "parking", "miejsce postojowe"]):
        filters["garaz"] = True

    return filters

st.title("🏠 Asystent Mieszkaniowy - Parser i Animowany placeholder")

placeholder_texts = [
    "Szukam mieszkania na Malcie...",
    "3 pokoje z balkonem...",
    "Cena do 750000 zł...",
    "Mieszkanie 4 pokoje w Wildzie",
    "70 m2 na Jeżycach z garażem"
]

placeholder = st.empty()
for text in placeholder_texts:
    input_text = placeholder.text_input("Wpisz swoje zapytanie:", value=text, key=text)
    time.sleep(1.5)
    placeholder.empty()

# Właściwe pole tekstowe
user_input = st.text_input("Twoje zapytanie:", "")

if user_input:
    filters = parse_user_input(user_input)
    st.write("🔍 Wydobyte parametry:")
    st.json(filters)
