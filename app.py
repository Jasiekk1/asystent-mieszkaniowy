
import streamlit as st
import pandas as pd
import re
from datetime import datetime

@st.cache_data
def load_data():
    return pd.read_csv("mieszkania.csv")

df = load_data()
df.columns = df.columns.str.strip().str.lower()

# Ekstrakcja informacji z zapytania użytkownika
def extract_filters(user_input):
    filters = {}
    loc_match = re.search(r"na\s+(\w+)", user_input.lower())
    if loc_match:
        filters["lokalizacja"] = loc_match.group(1)

    pokoje_match = re.search(r"(\d+)\s*pok", user_input.lower())
    if pokoje_match:
        filters["pokoje"] = int(pokoje_match.group(1))

    if "balkon" in user_input.lower():
        filters["balkon"] = True

    metraz_match = re.search(r"(\d+)\s*(m|m2|m²)", user_input.lower())
    if metraz_match:
        filters["metraz"] = int(metraz_match.group(1))

    return filters

# Filtracja mieszkań
def filter_offers(filters):
    results = df.copy()

    if "lokalizacja" in filters:
       results = results[results["lokalizacja"].str.lower().str.strip() == filters["lokalizacja"].lower()]

    if "pokoje" in filters:
        results = results[results["pokoje"] == filters["pokoje"]]

    if "balkon" in filters:
        results = results[results["balkon"] == True]

    if "metraz" in filters:
        results = results[(results["metraz"] >= filters["metraz"] - 5) & (results["metraz"] <= filters["metraz"] + 5)]

    return results

# Zapis konwersacji do pliku
def save_chat_log(chat):
    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_df = pd.DataFrame(chat, columns=["Kto", "Wiadomość"])
    log_df.to_csv(f"chat_log_{now}.csv", index=False)

# UI
st.set_page_config(page_title="Asystent Mieszkaniowy", layout="centered")
st.title("🏡 Asystent Mieszkaniowy (offline)")
st.write("Wpisz np. 'szukam 3 pokoi z balkonem na Jeżycach' lub '75 m2 na Malcie z balkonem'")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
    st.session_state.suggest_next = True

user_input = st.text_input("🧑 Ty:")

if user_input:
    st.session_state.chat_history.append(("Ty", user_input))
    filters = extract_filters(user_input)
    results = filter_offers(filters)

    if not results.empty:
        response = f"✅ Znalazłem {len(results)} ofert:"
        st.session_state.chat_history.append(("Bot", response))
        for _, row in results.iterrows():
            offer = f"{row['lokalizacja']} • {row['metraz']}m² • {row['pokoje']} pokoje • Balkon: {'Tak' if row['balkon'] else 'Nie'} • {row['cena']} zł"
            st.session_state.chat_history.append(("Bot", offer))
        st.session_state.suggest_next = False
    else:
        response = "❌ Nie znalazłem pasujących mieszkań. Może spróbuj zmienić lokalizację, liczbę pokoi lub metraż."
        st.session_state.chat_history.append(("Bot", response))
        st.session_state.suggest_next = True

# Sugestia dalszej rozmowy
if st.session_state.suggest_next:
    st.session_state.chat_history.append(("Bot", "💡 Napisz, ile pokoi Cię interesuje lub jaka lokalizacja."))

# Wyświetlenie historii czatu
st.markdown("### 💬 Historia rozmowy")
for kto, tekst in st.session_state.chat_history:
    st.markdown(f"**{kto}:** {tekst}")

# Zapisz konwersację
if st.button("💾 Zapisz rozmowę do pliku"):
    save_chat_log(st.session_state.chat_history)
    st.success("Rozmowa została zapisana!")
