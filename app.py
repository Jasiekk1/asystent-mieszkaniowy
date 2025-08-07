
import streamlit as st
import pandas as pd
import re

# === Wczytanie danych ===
@st.cache_data
def load_data():
    return pd.read_csv("mieszkania.csv")

df = load_data()

# === Funkcja pomocnicza do rozumienia zapytań użytkownika ===
def extract_filters(user_input):
    filters = {}

    # Lokalizacja (np. Malta, Rataje, Jeżyce)
    loc_match = re.search(r"na\s+(\w+)", user_input.lower())
    if loc_match:
        filters["lokalizacja"] = loc_match.group(1)

    # Liczba pokoi
    pokoje_match = re.search(r"(\d+)\s*pok", user_input.lower())
    if pokoje_match:
        filters["pokoje"] = int(pokoje_match.group(1))

    # Balkon
    if "balkon" in user_input.lower():
        filters["balkon"] = True

    # Metraż (np. "około 80m")
    metraz_match = re.search(r"(\d+)\s*(m|m2|m²)", user_input.lower())
    if metraz_match:
        filters["metraz"] = int(metraz_match.group(1))

    return filters

# === Filtrowanie danych ===
def filter_offers(filters):
    results = df.copy()

    if "lokalizacja" in filters:
        results = results[results["lokalizacja"].str.lower().str.contains(filters["lokalizacja"])]

    if "pokoje" in filters:
        results = results[results["pokoje"] == filters["pokoje"]]

    if "balkon" in filters:
        results = results[results["balkon"] == True]

    if "metraz" in filters:
        results = results[(results["metraz"] >= filters["metraz"] - 5) & (results["metraz"] <= filters["metraz"] + 5)]

    return results

# === Interfejs Streamlit ===
st.set_page_config(page_title="Asystent Mieszkaniowy AI", layout="centered")
st.title("🏠 Asystent mieszkaniowy AI")
st.write("Wpisz, czego szukasz:")

# Historia czatu (stan)
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Pole tekstowe użytkownika
user_input = st.text_input("💬 Twoje zapytanie", "")

# Po wprowadzeniu zapytania
if user_input:
    st.session_state.chat_history.append(("Ty", user_input))

    filters = extract_filters(user_input)
    results = filter_offers(filters)

    # Odpowiedź bota
    if not results.empty:
        response = f"✅ Znalazłem {len(results)} ofert:"
        st.session_state.chat_history.append(("Bot", response))

        for i, row in results.iterrows():
            offer_text = f"• {row['lokalizacja']}, {row['metraz']}m², {row['pokoje']} pok., balkon: {'tak' if row['balkon'] else 'nie'}, cena: {row['cena']} zł"
            st.session_state.chat_history.append(("Bot", offer_text))
    else:
        response = "❌ Niestety nie znalazłem ofert pasujących do Twojego zapytania."
        st.session_state.chat_history.append(("Bot", response))

# Wyświetlanie historii
st.markdown("### 🧠 Historia rozmowy")
for who, msg in st.session_state.chat_history:
    st.markdown(f"**{who}:** {msg}")
