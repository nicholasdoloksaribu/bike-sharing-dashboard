import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load datasets
day_df = pd.read_csv("https://raw.githubusercontent.com/nicholasdoloksaribu/bike-sharing-dashboard/refs/heads/main/data/day.csv")
hour_df = pd.read_csv("https://raw.githubusercontent.com/nicholasdoloksaribu/bike-sharing-dashboard/refs/heads/main/data/hour.csv")

# Mapping kondisi cuaca
weather_labels = {
    1: "Cerah",
    2: "Mendung",
    3: "Hujan"
}

day_df["weather_label"] = day_df["weathersit"].map(weather_labels)
hour_df["weather_label"] = hour_df["weathersit"].map(weather_labels)

# Hapus data NaN pada cuaca
day_df = day_df.dropna(subset=["weather_label"])
hour_df = hour_df.dropna(subset=["weather_label"])

# Pastikan kolom "hr" bertipe integer
hour_df["hr"] = hour_df["hr"].astype(int)

# === Sidebar Filters ===
st.sidebar.title("Filter Data")
analysis_type = st.sidebar.radio("Pilih Jenis Analisis:", ["Cuaca", "Jam"])

if analysis_type == "Cuaca":
    weather_options = ["Semua Cuaca"] + list(day_df["weather_label"].unique())
    selected_weathersit = st.sidebar.selectbox("Pilih Kondisi Cuaca:", weather_options)

    if selected_weathersit == "Semua Cuaca":
        filtered_day_df = day_df
    else:
        filtered_day_df = day_df[day_df["weather_label"] == selected_weathersit]

elif analysis_type == "Jam":
    selected_hour_range = st.sidebar.slider(
        "Pilih Rentang Jam:", 
        min_value=int(hour_df["hr"].min()), 
        max_value=int(hour_df["hr"].max()), 
        value=(0, 23)
    )
    filtered_day_df = day_df.copy()

# === Dashboard Title ===
st.title("Dashboard Analisis Bike Sharing")

# === 1. Statistik Penyewaan ===
st.subheader("Statistik Penyewaan Sepeda")
st.metric("Rata-rata Penyewaan Sepeda per Hari", round(filtered_day_df["cnt"].mean(), 2))
st.metric("Total Penyewaan Sepeda (Sesuai Filter)", filtered_day_df["cnt"].sum())

# === Analisis Berdasarkan Pilihan ===
if analysis_type == "Cuaca":
    st.subheader("Pengaruh Cuaca terhadap Penyewaan Sepeda")
    
    # Perbaikan agar cnt konsisten
    cuaca_grouped = day_df.groupby("weather_label")["cnt"].mean().reset_index()

    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(x="weather_label", y="cnt", data=cuaca_grouped, ax=ax, order=["Cerah", "Mendung", "Hujan"])
    plt.title("Pengaruh Cuaca terhadap Jumlah Penyewaan Sepeda")
    plt.xlabel("Kondisi Cuaca")
    plt.ylabel("Jumlah Sepeda Disewa")
    st.pyplot(fig)

elif analysis_type == "Jam":
    st.subheader("Pola Penyewaan Sepeda Berdasarkan Jam")

    # Filter data berdasarkan rentang jam
    hour_filtered = hour_df[(hour_df["hr"] >= selected_hour_range[0]) & (hour_df["hr"] <= selected_hour_range[1])]

    fig, ax = plt.subplots(figsize=(10, 5))
    sns.lineplot(x="hr", y="cnt", data=hour_filtered, estimator="mean")
    plt.xlabel("Jam")
    plt.ylabel("Jumlah Penyewaan")
    st.pyplot(fig)

# === Kesimpulan ===
st.subheader("Insight")
if analysis_type == "Cuaca":
    st.write("**Cuaca mempengaruhi jumlah penyewaan sepeda. Cuaca cerah meningkatkan penggunaan, sedangkan cuaca mendung dan hujan menurunkan tingkat penyewaan.**")

elif analysis_type == "Jam":
    st.write("**Pola penyewaan berdasarkan jam menunjukkan lonjakan pada jam sibuk pagi dan sore hari.**")
    st.write("**Pada jam non-sibuk, penggunaan sepeda cenderung lebih rendah.**")
