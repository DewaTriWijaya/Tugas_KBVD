import pandas as pd
import streamlit as st

# Load cleaned data
all_df = pd.read_csv("data/openaq_depok_clean.csv")

# Standarisasi nama kolom ke lowercase
all_df.columns = all_df.columns.str.lower()

# Konversi datetime & urutkan
all_df["datetimelocal"] = pd.to_datetime(all_df["datetimelocal"])
all_df.sort_values(by="datetimelocal", inplace=True)
all_df.reset_index(inplace=True)

# Filter data berdasarkan tanggal
min_date = all_df["datetimelocal"].min()
max_date = all_df["datetimelocal"].max()

with st.sidebar:
    st.image("https://raw.githubusercontent.com/DewaTriWijaya/Tugas_KBVD/refs/heads/main/logo.png")

    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

# Filter data berdasarkan rentang tanggal
main_df = all_df[(all_df["datetimelocal"] >= str(start_date)) & 
                 (all_df["datetimelocal"] <= str(end_date))]

# Hitung rata-rata kualitas udara berdasarkan parameter
avg_values = main_df.groupby("parameter")["value"].mean().round(2)

# Mengambil nilai rata-rata dengan aman (menggunakan .get() untuk menghindari error)
pm1_avg = avg_values.get("pm1", 0)
pm10_avg = avg_values.get("pm10", 0)
pm25_avg = avg_values.get("pm25", 0)
o3_avg = avg_values.get("O3", 0)

# Tampilkan dashboard
st.header('Dashboard Kualitas Udara Kota Depok')

# Tampilkan data tanggal yang dipilih dalam bentuk Senin 01 Januari 2021
st.subheader(f"Data dari {start_date:%A %d %B %Y} - {end_date:%A %d %B %Y}")


# Threshold values
thresholds = {
    "PM1": 15,    # Example threshold for PM1
    "PM10": 45,  # Example threshold for PM10
    "PM2.5": 15, # Example threshold for PM2.5
    "O3": 0.1     # Example threshold for O3
}

# Fungsi untuk membuat kartu dengan perubahan warna
def card(title, value, unit, threshold):
    color = "green" if value <= threshold else "red"
    st.markdown(
        f"""
        <div style="
            background-color: #ffffff;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 4px 4px 10px rgba(0,0,0,0.1);
            text-align: center;
            width: 100%;
            margin: 10px;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;">
            <h4 style="color: #555; margin: 0;">{title}</h4>
            <h2 style="color: {color}; margin: 5px 0;">{value} <span style="font-size: 18px; color: #777;">{unit}</span></h2>
            <p style="color: {color};">{'Warning: Exceeds threshold!' if color == 'red' else 'Value is safe'}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

# Gunakan Streamlit columns untuk mengatur layout dengan jarak antar kartu
col1, col2 = st.columns([1, 1])
with col1:
    card("Parameter PM1", pm1_avg, "µg/m³", thresholds["PM1"])

with col2:
    card("Parameter PM10", pm10_avg, "µg/m³", thresholds["PM10"])

col3, col4 = st.columns([1, 1])
with col3:
    card("Parameter PM2.5", pm25_avg, "µg/m³", thresholds["PM2.5"])

with col4:
    card("Parameter O3", o3_avg, "ppm", thresholds["O3"])


