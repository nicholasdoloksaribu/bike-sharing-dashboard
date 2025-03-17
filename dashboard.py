import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load datasets
day_df = pd.read_csv("https://raw.githubusercontent.com/nicholasdoloksaribu/bike-sharing-dashboard/refs/heads/main/data/day.csv")
hour_df = pd.read_csv("https://raw.githubusercontent.com/nicholasdoloksaribu/bike-sharing-dashboard/refs/heads/main/data/hour.csv")

# Mapping kondisi cuaca
weather_mapping = {1: "Cerah", 2: "Mendung", 3: "Hujan"}
day_df["weathersit"] = day_df["weathersit"].map(weather_mapping).fillna("Tidak Diketahui")
hour_df["weathersit"] = hour_df["weathersit"].map(weather_mapping).fillna("Tidak Diketahui")

day_df = day_df.dropna(subset=["weathersit"] )
hour_df = hour_df.dropna(subset=["weathersit"])

# Pastikan kolom "hr" bertipe integer
hour_df["hr"] = hour_df["hr"].astype(int)

# === Sidebar Filters ===
st.sidebar.title("🔍 Filter Data")
analysis_type = st.sidebar.radio("Pilih Jenis Analisis:", ["Cuaca", "Jam"])

if analysis_type == "Cuaca":
    selected_weathersit = st.sidebar.selectbox("Pilih Kondisi Cuaca:", hour_df["weathersit"].unique())
    filtered_data = hour_df[hour_df["weathersit"] == selected_weathersit]

elif analysis_type == "Jam":
    selected_hour_range = st.sidebar.slider("Pilih Rentang Jam:", min_value=int(hour_df["hr"].min()), max_value=int(hour_df["hr"].max()), value=(0, 23))
    filtered_data = hour_df[(hour_df["hr"] >= selected_hour_range[0]) & (hour_df["hr"] <= selected_hour_range[1])]

# === Dashboard Title ===
st.title("🚲 Dashboard Analisis Bike Sharing")

# === 1. Statistik Penyewaan ===
st.subheader("📊 Statistik Penyewaan Sepeda")
st.metric("Rata-rata Penyewaan Sepeda per Jam", round(hour_df["cnt"].mean(), 2))
st.metric("Total Penyewaan Sepeda (Sesuai Filter)", filtered_data["cnt"].sum())

# === Analisis Berdasarkan Pilihan ===
if analysis_type == "Cuaca":
    st.subheader("☁️ Pengaruh Cuaca terhadap Penyewaan Sepeda")
    cuaca_grouped = hour_df.groupby("weathersit")["cnt"].sum().reset_index()
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(x="weathersit", y="cnt", data=cuaca_grouped, ax=ax)
    plt.xlabel("Kondisi Cuaca")
    plt.ylabel("Total Penyewaan Sepeda")
    st.pyplot(fig)
    
elif analysis_type == "Jam":
    st.subheader("⏰ Pola Penyewaan Sepeda Berdasarkan Jam")
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.lineplot(x="hr", y="cnt", data=filtered_data, ci=None, ax=ax)
    plt.xlabel("Jam")
    plt.ylabel("Jumlah Penyewaan")
    st.pyplot(fig)

# === Kesimpulan ===
st.subheader("Insight")
if analysis_type == "Cuaca":
    st.write("**Cuaca mempengaruhi jumlah penyewaan sepeda, dengan kondisi cerah meningkatkan penggunaan  dan cuaca mendung dan hujan menurunkan tingkat penyewaan sepeda.**")
  
elif analysis_type == "Jam":
    st.write("**Pola penyewaan berdasarkan jam menunjukkan lonjakan pada jam sibuk pagi dan sore hari.**")
    st.write("**Pada jam non-sibuk, penggunaan sepeda cenderung lebih rendah.**")
