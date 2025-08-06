
import streamlit as st
import pandas as pd

# Wczytaj dane
df = pd.read_csv("mieszkania.csv")

st.title("🏠 Asystent mieszkaniowy AI")

query = st.text_input("Czego szukasz? (np. 3 pokoje z balkonem na Malcie)")

if query:
    st.write("🔍 Przetwarzam zapytanie:", query)

    # Prosty filtr (w demo bez AI)
    if "Malta" in query:
        df = df[df["Lokalizacja"].str.contains("Malta")]
    if "balkon" in query.lower():
        df = df[df["Balkon"] == "Tak"]
    if "3" in query and "pok" in query:
        df = df[df["Pokoje"] == 3]
    if "4" in query and "pok" in query:
        df = df[df["Pokoje"] == 4]

    st.subheader("📋 Znalezione mieszkania:")
    st.dataframe(df)

    if not df.empty:
        st.success(f"✅ Rekomenduję mieszkanie na {df.iloc[0]['Lokalizacja']} o powierzchni {df.iloc[0]['Metraż']} m².")
    else:
        st.warning("Nie znaleziono ofert pasujących do zapytania.")
else:
    st.info("Wpisz czego szukasz, np. '3 pokoje z balkonem na Malcie'")
