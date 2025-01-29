import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
sns.set(style='dark')

# Load cleaned data
all_df = pd.read_csv("data/openaq_depok_clean.csv")

datetime_columns = ["datetimeLocal"]
all_df.sort_values(by="datetimeLocal", inplace=True)
all_df.reset_index(inplace=True)

for column in datetime_columns:
    all_df[column] = pd.to_datetime(all_df[column])

# Filter data
min_date = all_df["datetimeLocal"].min()
max_date = all_df["datetimeLocal"].max()

with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://raw.githubusercontent.com/DewaTriWijaya/ImageAsset/refs/heads/main/logo.png")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = all_df[(all_df["datetimeLocal"] >= str(start_date)) & 
                (all_df["datetimeLocal"] <= str(end_date))]


# plot number of daily sharing (2011)
st.header('Bike Sharing Collection Dashboard :sparkles:')
st.subheader('Daily Sharing')
