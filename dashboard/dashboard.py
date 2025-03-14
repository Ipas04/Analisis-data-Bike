import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

day_df = pd.read_csv('main_data.csv')

sns.set_theme(style="whitegrid")

st.title("Analisis Penyewaan Sepeda Kasual Berdasarkan Musim, Hari Libur, dan Hari Kerja")

st.write("Dashboard ini memudahkan pengguna untuk memilih musim dan melihat jumlah penyewaan sepeda kasual berdasarkan hari kerja dan akhir pekan.")

season_labels = ['Spring', 'Summer', 'Fall', 'Winter']

with st.sidebar:
    st.header("Pilih Musim")
    selected_season = st.selectbox("Musim", season_labels, index=0)

# Mendapatkan nomor musim berdasarkan pilihan
season_number = season_labels.index(selected_season) + 1

# Filter data berdasarkan musim yang dipilih
data_filtered = day_df[day_df['season'] == season_number]

# permusim
seasonal_casual_rentals = data_filtered.groupby('season')['casual'].sum()

# seluruh musim
seasonal = day_df.groupby('season')['casual'].sum()

# Membuat grafik batang untuk jumlah penyewaan kasual per musim
fig, ax = plt.subplots()
season_names = ['Spring', 'Summer', 'Fall', 'Winter']
casual_rentals_bars = ax.bar(season_names, [seasonal.get(season_number, 0) for season_number in range(1, 5)], color=['lightblue', 'lightgreen', 'orange', 'grey'])
ax.set_ylabel('Total Penyewaan Kasual')
ax.set_title('Total Penyewaan Kasual per Musim')
ax.set_facecolor('#f5f5f5')

for bar in casual_rentals_bars:
    yval = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, yval, round(yval, 2), va='bottom')
st.pyplot(fig)


if not data_filtered.empty:
    working_day_data = data_filtered[data_filtered['workingday'] == 1]['casual'].sum()
    weekend_data = data_filtered[data_filtered['workingday'] == 0]['casual'].sum()

    # Membuat grafik batang untuk hari kerja vs akhir pekan (penyewaan)
    fig, ax = plt.subplots()
    bars = ax.bar(['Hari Kerja', 'Akhir Pekan'], [working_day_data, weekend_data], color=['tomato', 'deepskyblue'])
    for bar in bars:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, yval, round(yval, 2), va='bottom') 
    ax.set_ylabel('Jumlah Penyewaan Kasual')
    ax.set_title(f'Penyewaan Kasual pada {selected_season} (Hari Kerja vs Akhir Pekan)')
    ax.set_facecolor('#f5f5f5')  
    st.pyplot(fig)

    # Kelompokkan data berdasarkan weather_isit dan hitung jumlah penyewaan kasual
    weather_casual_rentals = data_filtered.groupby('weathersit')['casual'].sum()

    # Membuat grafik batang untuk jumlah penyewaan kasual berdasarkan weatherst pada musim yang dipilih
    fig, ax = plt.subplots()
    weather_labels = ['Clear', 'Mist', 'Light Rain', 'Heavy Rain']
    weather_bars = ax.bar(weather_labels, [weather_casual_rentals.get(i, 0) for i in range(1, 5)], color=['skyblue', 'lightgray', 'lightblue', 'dimgrey'])
    ax.set_ylabel('Total Penyewaan Kasual')
    ax.set_title(f'Total Penyewaan Kasual Season {selected_season}')
    ax.set_facecolor('#f5f5f5')

    for bar in weather_bars:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, yval, round(yval, 2), va='bottom')
    st.pyplot(fig)

else:
    st.error("Tidak ada data untuk musim yang dipilih.")
