import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

st.set_option('deprecation.showPyplotGlobalUse', False)
all_df = pd.read_csv("submission\\Dataset\\all_data.csv")

# Fungsi untuk menampilkan plot kualitas udara tiap bulannya
def plot_by_month(air_df):
    plt.figure(figsize=(10, 6))
    sns.lineplot(data=air_df, x='month', y='Air_condition', hue='station', marker='o')
    plt.title('Tren Kualitas Udara per Bulan')
    plt.xlabel('Bulan')
    plt.ylabel('Air Condition')
    plt.legend(title='Stasiun')
    plt.grid(True)
    st.pyplot()

# Fungsi untuk menampilkan grafik pengaruh hujan
def plot_rain_distribution(df):
    plt.figure(figsize=(10, 6))
    sns.histplot(data=rain_df, x=df['All Particles'], hue='RAIN', kde=True, bins=30, alpha=0.5)
    plt.xlabel('Semua Partikel')
    plt.ylabel('Frekuensi')
    plt.title('Distribusi Semua Partikel saat Hujan dan Tidak Hujan')
    plt.legend(title='Rain', loc='upper right')
    st.pyplot()

# Main function
def main():
    
    #sidebar 

    with st.sidebar:
        # Menambahkan logo perusahaan
        st.image("https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.pinterest.com%2Fpin%2F519813981995570794%2F&psig=AOvVaw0iKJQvng8if04Yf6qJvPVQ&ust=1709716071352000&source=images&cd=vfe&opi=89978449&ved=0CBIQjRxqFwoTCLiD5-ri3IQDFQAAAAAdAAAAABAJ")
        
        # Sidebar untuk memilih opsi plot
        plot_option = st.sidebar.selectbox("Pilih Grafik", ["Grafik Setiap Stasiun", "Grafik pengaruh hujan terhadap polutan"])
    
    if plot_option == "Grafik Setiap Stasiun":
        st.title('Analisis Kualitas Udara')
        # Menampilkan dropdown untuk memilih stasiun
        selected_station = st.selectbox("Pilih Stasiun", air_df['station'].unique())
        
        # Menampilkan plot berdasarkan stasiun yang dipilih
        plot_by_station(selected_station, air_df)
        
        st.subheader('Plot kualitas udara tiap bulannya')
        plot_by_month(air_df)
        
    elif plot_option == "Grafik pengaruh hujan terhadap polutan":
        st.title('pengaruh hujan terhadap polutan')
        # Menampilkan plot distribusi partikel saat hujan dan tidak hujan
        plot_rain_distribution(df)

def determine_air_condition(row):
    if row['PM2.5'] <= 50 and row['PM10'] <= 50 and row['SO2'] <= 20 and row['NO2'] <= 40 and row['CO'] <= 1000 and row['O3'] <= 80:
        return "Baik"
    elif row['PM2.5'] <= 100 and row['PM10'] <= 50 and row['SO2'] <= 40 and row['NO2'] <= 100 and row['CO'] <= 2000 and row['O3'] <= 160:
        return "Sedang"
    elif row['PM2.5'] <= 250 and row['PM10'] <= 100 and row['SO2'] <= 200 and row['NO2'] <= 200 and row['CO'] <= 10000 and row['O3'] <= 200:
        return "Tidak Sehat"
    elif row['PM2.5'] <= 350 and row['PM10'] <= 250 and row['SO2'] <= 300 and row['NO2'] <= 400 and row['CO'] <= 17000 and row['O3'] <= 250:
        return "Sangat Tidak Sehat"
    else:
        return "Berbahaya"
    
def plot_by_station(selected_station, air_df):
    st.subheader(f"Plot untuk Stasiun {selected_station}")
    plot_data = air_df[air_df['station'] == selected_station]
    sns.catplot(x="year", hue="Air_condition", kind="count", data=plot_data, col="station")
    st.pyplot()

# EDA
#membuat data daily
daily_df = all_df.groupby(by=["station", "year","month","day"]).agg({
    "PM2.5": "max",
    "PM10": "max",
    "SO2": "max",
    "NO2": "max",
    "CO": "max",
    "O3": "max"
})
daily_df.reset_index(inplace=True)

#Visualisasi data
##menampilkan grafik udara di stasiun cina
###explanatory analisis kondisi udara
air_df= daily_df.copy()


air_df['Air_condition'] = air_df.apply(determine_air_condition, axis=1)

# Data hujan untuk contoh
rain_df = all_df.copy()

# Konversi kolom RAIN menjadi biner (0 untuk tidak hujan, 1 untuk hujan)


# Memilih kolom yang akan dianalisis
kolom_udara = ['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3']

# Membuat DataFrame untuk kondisi udara saat hujan dan tidak hujan
rain = rain_df[rain_df['RAIN'] == 1][kolom_udara]
not_rain = rain_df[rain_df['RAIN'] == 0][kolom_udara]


df = pd.concat([rain, not_rain], ignore_index=True)
df['All Particles'] = df[['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3']].sum(axis=1)



if __name__ == "__main__":
    main()