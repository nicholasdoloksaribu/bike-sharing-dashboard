import streamlit as st
import pandas as pd

st.title("Dashboard Bike Sharing Dataset")

url_day = 'https://raw.githubusercontent.com/nicholasdoloksaribu/bike-sharing-dashboard/refs/heads/main/data/day.csv';
url_hour = 'https://raw.githubusercontent.com/nicholasdoloksaribu/bike-sharing-dashboard/refs/heads/main/data/hour.csv'

# Load dataset
day_df = pd.read_csv( url_day)
hour_df = pd.read_csv(url_hour)

st.write("Tampilan Data Awal:")
st.dataframe(day_df.head())

option = st.selectbox("Pilih Grafik", ["Cuaca vs Penyewaan", "Penyewaan berdasarkan Jam"])

if option == "Cuaca vs Penyewaan":
    st.bar_chart(day_df.groupby("weathersit")["cnt"].mean())

elif option == "Penyewaan berdasarkan Jam":
    st.line_chart(hour_df.groupby("hr")["cnt"].mean())
