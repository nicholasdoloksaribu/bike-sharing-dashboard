import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load datasets
day_df = pd.read_csv("day.csv")
hour_df = pd.read_csv("hour.csv")

# Mapping kondisi cuaca (Hapus kategori 4 & "Tidak Diketahui")
weather_mapping = {1: "Cerah", 2: "Mendung", 3: "Hujan"}
day_df["weathersit"] = day_df["weathersit"].map(weather_mapping)
hour_df["weathersit"] = hour_df["weathersit"].map(weather_mapping)

# Hapus data dengan nilai NaN di kolom weathersit agar "Tidak Diketahui" tidak masuk filter
day_df = day_df.dropna(subset=["weathersit"])
hour_df = hour_df.dropna(subset=["weathersit"])

# Pastikan kolom "hr" bertipe integer
hour_df["hr"] = hour_df["hr"].astype(int)

# === Sidebar Filters ===
st.sidebar.title("Filter Data")
analysis_type = st.sidebar.radio("Pilih Jenis Analisis:", ["Cuaca", "Jam"])

if analysis_type == "Cuaca":
    selected_weathersit = st.sidebar.selectbox("Pilih Kondisi Cuaca:", day_df["weathersit"].unique())
    
    # Filter data untuk cuaca
    filtered_day_df = day_df[day_df["weathersit"] == selected_weathersit]
    filtered_hour_df = hour_df[hour_df["weathersit"] == selected_weathersit]

elif analysis_type == "Jam":
    selected_hour_range = st.sidebar.slider("Pilih Rentang Jam:", min_value=int(hour_df["hr"].min()), max_value=int(hour_df["hr"].max()), value=(0, 23))
    
    # Filter data untuk jam
    filtered_day_df = day_df.copy()  # Tidak ada filter khusus untuk day_df dalam mode ini
    filtered_hour_df = hour_df[(hour_df["hr"] >= selected_hour_range[0]) & (hour_df["hr"] <= selected_hour_range[1])]

# === Dashboard Title ===
st.title("Dashboard Analisis Bike Sharing")

# === 1. Statistik Penyewaan ===
st.subheader("Statistik Penyewaan Sepeda")
st.metric("Rata-rata Penyewaan Sepeda per Jam", round(filtered_hour_df["cnt"].mean(), 2))
st.metric("Total Penyewaan Sepeda (Sesuai Filter)", filtered_hour_df["cnt"].sum())

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
    st.subheader("Pola Penyewaan Sepeda Berdasarkan Jam")
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.lineplot(x="hr", y="cnt", data=filtered_hour_df, ci=None, ax=ax)
    plt.xlabel("Jam")
    plt.ylabel("Jumlah Penyewaan")
    st.pyplot(fig)

# === Kesimpulan ===
st.subheader("Insight")
if analysis_type == "Cuaca":
    st.write("**Cuaca mempengaruhi jumlah penyewaan sepeda, dengan kondisi cerah meningkatkan penggunaan dan cuaca mendung serta hujan menurunkan tingkat penyewaan sepeda.**")
  
elif analysis_type == "Jam":
    st.write("**Pola penyewaan berdasarkan jam menunjukkan lonjakan pada jam sibuk pagi dan sore hari.**")
    st.write("**Pada jam non-sibuk, penggunaan sepeda cenderung lebih rendah.**")
