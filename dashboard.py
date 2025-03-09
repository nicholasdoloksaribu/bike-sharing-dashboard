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

# Kategori Hari
week_mapping = {0: "Senin", 1: "Selasa", 2: "Rabu", 3: "Kamis", 4: "Jumat", 5: "Sabtu", 6: "Minggu"}
day_df["Kategori Hari"] = day_df["weekday"].map(week_mapping)

# === Sidebar Filters ===
st.sidebar.title("🔍 Filter Data")
selected_weathersit = st.sidebar.selectbox("Pilih Kondisi Cuaca:", day_df["weathersit"].unique())
selected_day_category = st.sidebar.selectbox("Pilih Hari:", day_df["Kategori Hari"].unique())
selected_hour = st.sidebar.slider("Pilih Jam:", min_value=int(hour_df["hr"].min()), max_value=int(hour_df["hr"].max()), value=(0, 23))

# Filter dataset
day_filtered = day_df[(day_df["weathersit"] == selected_weathersit) & (day_df["Kategori Hari"] == selected_day_category)]
hour_filtered = hour_df[(hour_df["weathersit"] == selected_weathersit) & (hour_df["hr"].between(selected_hour[0], selected_hour[1]))]

# === Dashboard Title ===
st.title("Dashboard Analisis Bike Sharing")

# === 1. Statistik Penyewaan ===
st.subheader("Statistik Penyewaan Sepeda")
st.metric("Total Penyewaan Sepeda pada Hari Terpilih", day_filtered["cnt"].sum())
st.metric("Rata-rata Penyewaan Sepeda", round(day_filtered["cnt"].mean(), 2))
st.metric("Total Penyewaan Sepeda pada Jam Terpilih", hour_filtered["cnt"].sum())

# === 2. Distribusi Penyewaan Sepeda ===
st.subheader("Distribusi Penyewaan Sepeda")
fig, ax = plt.subplots(figsize=(8,5))
sns.histplot(day_filtered["cnt"], bins=30, kde=True, color='blue', ax=ax)
plt.xlabel("Jumlah Penyewaan Sepeda")
plt.ylabel("Frekuensi")
st.pyplot(fig)

# === 3. Pengaruh Cuaca terhadap Penyewaan ===
st.subheader("☁️ Pengaruh Cuaca terhadap Penyewaan Sepeda")
fig, ax = plt.subplots(figsize=(8,5))
sns.barplot(x="weathersit", y="cnt", data=day_filtered, ax=ax)
plt.xlabel("Kondisi Cuaca")
plt.ylabel("Jumlah Penyewaan Sepeda")
st.pyplot(fig)

# === 4. Pola Penyewaan Berdasarkan Hari ===
st.subheader("Pola Penyewaan Sepeda Berdasarkan Hari")
fig, ax = plt.subplots(figsize=(10,5))
sns.barplot(x="Kategori Hari", y="cnt", data=day_filtered, palette="Set2", ax=ax)
plt.xlabel("Kategori Hari")
plt.ylabel("Jumlah Penyewaan")
st.pyplot(fig)

# === 5. Pola Penyewaan Berdasarkan Jam ===
st.subheader("Pola Penyewaan Sepeda Berdasarkan Jam")
fig, ax = plt.subplots(figsize=(10,5))
sns.lineplot(x="hr", y="cnt", data=hour_filtered, estimator="mean", ax=ax)
plt.xlabel("Jam")
plt.ylabel("Jumlah Penyewaan")
st.pyplot(fig)

# === Kesimpulan ===
st.subheader("Kesimpulan")
st.write("✅ **Cuaca mempengaruhi jumlah penyewaan sepeda, dengan kondisi cerah meningkatkan penggunaan.**")
st.write("✅ **Hari kerja cenderung memiliki jumlah penyewaan lebih tinggi dibanding akhir pekan.**")
st.write("✅ **Kategori cuaca mendung atau hujan menurunkan tingkat penyewaan sepeda.**")
st.write("✅ **Pola penyewaan berdasarkan jam menunjukkan lonjakan pada jam sibuk pagi dan sore hari.**")
