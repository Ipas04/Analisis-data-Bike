import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

sns.set(style='dark')

day_df = pd.read_csv('main_data.csv')
day_df['dteday'] = pd.to_datetime(day_df['dteday'])


months = [
    "Januari", "Februari", "Maret", "April", "Mei", "Juni",
    "Juli", "Agustus", "September", "Oktober", "November", "Desember"
]

day_df['yr'] = day_df['yr'].replace({0: 2011, 1: 2012})

with st.sidebar:
    st.header("Silahkan pilih kategori")
    selected_year = st.number_input("Pilih Tahun", min_value=2011, max_value=2012, value=2011)
    start_month = st.selectbox("Pilih Bulan Mulai", months)
    end_month = st.selectbox("Pilih Bulan Akhir", months)

month_to_number = {month: index + 1 for index, month in enumerate(months)}
start_month_number = month_to_number[start_month]
end_month_number = month_to_number[end_month]

data_filtered = day_df[
    (day_df['yr'] == selected_year) & 
    (day_df['mnth'] >= start_month_number) & 
    (day_df['mnth'] <= end_month_number)
]

st.header(f"Data Penyewaan dari Bulan {start_month} sampai {end_month} Tahun {selected_year}")

if data_filtered.empty:
    st.write("Maaf, data tidak ada untuk rentang bulan dan tahun ini.")
else:
    monthly_rentals = data_filtered.groupby(['mnth', 'yr']).agg({
        'cnt': 'sum', 
        'casual': 'sum', 
        'registered': 'sum'}).reset_index()

    month_labels = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    monthly_rentals['mnth'] = monthly_rentals['mnth'].apply(lambda x: month_labels[x - 1])

    max_value = monthly_rentals['cnt'].max()
    colors = ['red' if cnt == max_value else 'skyblue' for cnt in monthly_rentals['cnt']]

    # Membuat grafik jumlah penyewaan
    plt.figure(figsize=(10, 5))
    sns.barplot(x='mnth', y='cnt', data=monthly_rentals, palette=colors)

    plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x:,.0f}'))
    plt.xlabel("Bulan")
    plt.ylabel("Jumlah Penyewaan")
    plt.title(f"Jumlah Penyewaan Sepeda dari Bulan {start_month} sampai {end_month} Tahun {selected_year}")
    st.pyplot(plt)

    plt.figure(figsize=(10, 5))
    monthly_rentals.set_index('mnth')[['casual', 'registered']].plot(kind='bar', color=['skyblue', 'orange'])

    plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x:,.0f}'))
    plt.xlabel("Bulan")
    plt.ylabel("Jumlah Penyewaan")
    plt.title(f"Perbandingan Penyewaan Sepeda Casual dan Registered dari Bulan {start_month} sampai {end_month} Tahun {selected_year}")
    plt.xticks(rotation=45)
    st.pyplot(plt)

st.caption("Dashboard Penyewaan Sepeda | Siapang 2025")
