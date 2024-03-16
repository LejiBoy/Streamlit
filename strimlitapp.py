import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def gather_data(file_path):
    try:
        # Membaca data dari file CSV
        dataframe = pd.read_csv(file_path, usecols=['instant', 'dteday', 'hr', 'season', 'yr', 'mnth', 'holiday', 'weekday', 'workingday', 'weathersit', 'temp', 'atemp', 'hum', 'windspeed', 'casual', 'registered', 'cnt'])
        return dataframe
    except FileNotFoundError:
        st.error(f"File {file_path} not found.")
        return None
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None

# Load data
bike_data = gather_data('hour.csv')

if bike_data is not None:
    # Set page title
    st.title("Bike Sharing Analysis Dashboard")

    # Filter Options
    st.header("Filter Options")

    # Date and Time Selection
    min_date = pd.to_datetime(bike_data['dteday'].min()).date()
    max_date = pd.to_datetime(bike_data['dteday'].max()).date()
    selected_date = st.date_input("Select Date", min_value=min_date, max_value=max_date, value=min_date)
    selected_hour = st.slider("Select Hour", 0, 23)

    # Filtering data based on selected date and hour
    filtered_bike_data = bike_data[(bike_data['dteday'] == selected_date.strftime('%Y-%m-%d')) & (bike_data['hr'] == selected_hour)]

    # Display filtered data
    st.subheader("Filtered Data")
    st.write(filtered_bike_data)

    # Visualizations
    st.header("Visualizations")

    # Bar plot for bike rentals based on season
    st.subheader("Total Bike Rentals by Season")
    season_counts = bike_data.groupby('season')['cnt'].sum().reset_index()
    plt.figure(figsize=(10, 6))
    sns.barplot(data=season_counts, x='season', y='cnt', palette='viridis')
    plt.title("Total Bike Rentals by Season")
    plt.xlabel("Season")
    plt.ylabel("Total Rentals")
    st.pyplot(plt.gcf())

    # Scatter plot for temperature vs bike rentals
    st.subheader("Temperature vs Bike Rentals")
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=bike_data, x='temp', y='cnt', hue='season', palette='viridis')
    plt.title("Temperature vs Bike Rentals")
    plt.xlabel("Temperature (Celsius)")
    plt.ylabel("Total Rentals")
    st.pyplot(plt.gcf())

    # Line plot for hourly bike rentals
    st.subheader("Average Hourly Bike Rentals")
    hourly_rentals = bike_data.groupby('hr')['cnt'].mean().reset_index()
    plt.figure(figsize=(10, 6))
    sns.lineplot(data=hourly_rentals, x='hr', y='cnt', marker='o', color='red')
    plt.title("Average Hourly Bike Rentals")
    plt.xlabel("Hour")
    plt.ylabel("Count")
    st.pyplot(plt.gcf())

    # Bar plot for bike rentals based on weather situation
    st.subheader("Total Bike Rentals by Weather Situation")
    weather_counts = bike_data.groupby('weathersit')['cnt'].sum().reset_index()
    plt.figure(figsize=(10, 6))
    sns.barplot(data=weather_counts, x='weathersit', y='cnt', palette='viridis')
    plt.title("Total Bike Rentals by Weather Situation")
    plt.xlabel("Weather Situation")
    plt.ylabel("Total Rentals")
    st.pyplot(plt.gcf())

    # Bar plot for bike rentals based on user type
    st.subheader("Total Bike Rentals by User Type")
    user_counts = bike_data[['casual', 'registered']].sum().reset_index()
    user_counts.columns = ['user_type', 'total_rentals']
    plt.figure(figsize=(10, 6))
    sns.barplot(data=user_counts, x='user_type', y='total_rentals', palette='flare')
    plt.title("Total Bike Rentals by User Type")
    plt.xlabel("User Type")
    plt.ylabel("Total Rentals")
    st.pyplot(plt.gcf())

    # Bar plot for bike rentals based on month
    st.subheader("Total Bike Rentals by Month")
    month_counts = bike_data.groupby('mnth')['cnt'].sum().reset_index()
    plt.figure(figsize=(10, 6))
    sns.barplot(data=month_counts, x='mnth', y='cnt', palette='cubehelix')
    plt.title("Total Bike Rentals by Month")
    plt.xlabel("Month")
    plt.ylabel("Total Rentals")
    st.pyplot(plt.gcf())

    # Bar plot for bike rentals based on year
    st.subheader("Total Bike Rentals by Year")
    year_counts = bike_data.groupby('yr')['cnt'].sum().reset_index()
    year_counts['yr'] = year_counts['yr'].map({0: '2011', 1: '2012'})
    plt.figure(figsize=(8, 5))
    sns.barplot(data=year_counts, x='yr', y='cnt', palette='twilight')
    plt.title("Total Bike Rentals by Year")
    plt.xlabel("Year")
    plt.ylabel("Total Rentals")
    st.pyplot(plt.gcf())

    # Bar plot for bike rentals based on holiday
    st.subheader("Total Bike Rentals on Holidays")
    holiday_counts = bike_data.groupby('holiday')['cnt'].sum().reset_index()
    holiday_counts['holiday'] = holiday_counts['holiday'].map({0: 'No', 1: 'Yes'})
    plt.figure(figsize=(8, 5))
    sns.barplot(data=holiday_counts, x='holiday', y='cnt', palette='husl')
    plt.title("Total Bike Rentals on Holidays")
    plt.xlabel("Holiday")
    plt.ylabel("Total Rentals")
    st.pyplot(plt.gcf())

    # Bar plot for bike rentals based on working day
    st.subheader("Total Bike Rentals on Working Days")
    workingday_counts = bike_data.groupby('workingday')['cnt'].sum().reset_index()
    workingday_counts['workingday'] = workingday_counts['workingday'].map({0: 'No', 1: 'Yes'})
    plt.figure(figsize=(8, 5))
    sns.barplot(data=workingday_counts, x='workingday', y='cnt', palette='viridis')
    plt.title("Total Bike Rentals on Working Days")
    plt.xlabel("Working Day")
    plt.ylabel("Total Rentals")
    st.pyplot(plt.gcf())

    # Menampilkan lima baris pertama dari data sebelum pembersihan
    st.subheader("Data Sebelum Pembersihan")
    st.write(bike_data.head())

    # Memeriksa dan mengatasi nilai-nilai duplikat
    jumlah_duplikat = bike_data.duplicated().sum()
    if jumlah_duplikat > 0:
        st.write(f"Jumlah nilai duplikat sebelum penghapusan: {jumlah_duplikat}")
        bike_data.drop_duplicates(inplace=True)
        st.write("Nilai duplikat telah dihapus.")

    # Memeriksa dan mengatasi nilai-nilai yang hilang (NaN)
    st.subheader("Jumlah Nilai yang Hilang untuk Setiap Kolom:")
    st.write(bike_data.isnull().sum())

    # Menggantikan nilai-nilai yang hilang dengan nilai rata-rata kolom
    kolom_numerik = bike_data.select_dtypes(include='number').columns
    bike_data[kolom_numerik] = bike_data[kolom_numerik].fillna(bike_data[kolom_numerik].mean())

    # Menampilkan lima baris pertama dari data setelah pembersihan
    st.subheader("Data Setelah Pembersihan")
    st.write(bike_data.head())

    # Menampilkan informasi umum tentang dataset
    st.subheader("Informasi Data:")
    st.write(bike_data.info())

    # Menampilkan statistik deskriptif untuk data numerik
    st.subheader("Statistik Deskriptif:")
    st.write(bike_data.describe())

    # Menampilkan beberapa contoh data
    st.subheader("Contoh Data:")
    st.write(bike_data.head())

    # Menampilkan jumlah nilai yang unik untuk setiap kolom
    st.subheader("Jumlah Nilai Unik untuk Setiap Kolom:")
    st.write(bike_data.nunique())

    # Memeriksa nilai-nilai yang hilang
    st.subheader("Total Nilai Hilang untuk Setiap Kolom:")
    st.write(bike_data.isnull().sum())

    # Memeriksa nilai-nilai yang duplikat
    st.subheader("Total Nilai Duplikat:")
    st.write(bike_data.duplicated().sum())

    # Memeriksa korelasi antara variabel numerik
    st.subheader("Korelasi Antar Variabel Numerik:")
    kolom_numerik = ['temp', 'atemp', 'hum', 'windspeed', 'casual', 'registered', 'cnt']
    bike_data_numerik = bike_data[kolom_numerik]
    korelasi = bike_data_numerik.corr()
    plt.figure(figsize=(10, 8))
    sns.heatmap(korelasi, annot=True, cmap='viridis', fmt=".2f", linewidths=0.5)
    plt.title('Korelasi Antar Variabel Numerik')
    st.pyplot(plt.gcf())

    # Menampilkan lima baris pertama dari data
    st.subheader("Data Awal:")
    st.write(bike_data.head())

    # Informasi umum tentang dataset
    st.subheader("Informasi Dataset:")
    st.write(bike_data.info())

    # Statistik deskriptif untuk data numerik
    st.subheader("Statistik Deskriptif untuk Data Numerik:")
    st.write(bike_data.describe())

    # Jumlah nilai unik untuk setiap kolom
    st.subheader("Jumlah Nilai Unik untuk Setiap Kolom:")
    st.write(bike_data.nunique())

    # Memeriksa nilai-nilai yang hilang
    st.subheader("Total Nilai Hilang untuk Setiap Kolom:")
    st.write(bike_data.isnull().sum())

    # Memeriksa nilai-nilai yang duplikat
    st.subheader("Total Nilai Duplikat:")
    st.write(bike_data.duplicated().sum())

    # Visualisasi distribusi variabel numerik
    st.subheader("Distribusi Variabel Numerik")
    plt.figure(figsize=(15, 10))
    kolom_numerik = ['temp', 'atemp', 'hum', 'windspeed', 'casual', 'registered', 'cnt']
    for i, kolom in enumerate(kolom_numerik, 1):
        plt.subplot(3, 3, i)
        sns.histplot(bike_data[kolom], bins=20, kde=True)
        plt.title(f'Distribusi {kolom}')
    plt.tight_layout()
    st.pyplot(plt.gcf())

    # Korelasi antar variabel numerik
    st.subheader("Korelasi Antar Variabel Numerik")
    plt.figure(figsize=(10, 8))
    sns.heatmap(bike_data[kolom_numerik].corr(), annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5)
    plt.title('Korelasi Antar Variabel Numerik')
    st.pyplot(plt.gcf())

    # Visualisasi relasi antara variabel numerik
    st.subheader("Scatter Plot Antar Variabel Numerik")
    sns.pairplot(bike_data[kolom_numerik])
    plt.suptitle('Scatter Plot Antar Variabel Numerik', y=1.02)
    st.pyplot(plt.gcf())

    # Menampilkan informasi dataset
    st.subheader("Informasi Dataset")
    st.write(bike_data.info())

    # Memeriksa apakah ada nilai yang hilang dalam dataset
    st.subheader("Total Nilai Hilang untuk Setiap Kolom")
    st.write(bike_data.isnull().sum())

    # Membuat plot untuk membandingkan pola peminjaman sepeda antara hari-hari libur dan hari kerja
    st.subheader("Perbandingan Pola Peminjaman Sepeda antara Hari Libur dan Hari Kerja")
    plt.figure(figsize=(12, 6))
    sns.lineplot(x='hr', y='cnt', data=bike_data, hue='holiday', ci=None)
    plt.title('Perbandingan Pola Peminjaman Sepeda antara Hari Libur dan Hari Kerja')
    plt.xlabel('Jam (hr)')
    plt.ylabel('Jumlah Peminjaman Sepeda (cnt)')
    plt.xticks(range(24))
    plt.legend(['Bukan Hari Libur', 'Hari Libur'])
    st.pyplot(plt.gcf())

    # Set page title
    st.title("Bike Sharing Analysis Dashboard")

    # Menambahkan kolom baru untuk musim
    season_mapping = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
    bike_data['season_name'] = bike_data['season'].map(season_mapping)

    # Menampilkan informasi dataset
    st.subheader("Total Nilai Hilang untuk Setiap Kolom")
    st.write(bike_data.isnull().sum())

    # Membuat plot untuk membandingkan pola peminjaman sepeda berdasarkan musim dan jam dalam sehari
    st.subheader("Pola Peminjaman Sepeda Berdasarkan Musim dan Jam dalam Sehari")
    plt.figure(figsize=(12, 6))
    sns.lineplot(x='hr', y='cnt', data=bike_data, hue='season_name', ci=None)
    plt.title('Pola Peminjaman Sepeda Berdasarkan Musim dan Jam dalam Sehari')
    plt.xlabel('Jam (hr)')
    plt.ylabel('Jumlah Peminjaman Sepeda (cnt)')
    plt.xticks(range(24))
    plt.legend(title='Musim')
    st.pyplot(plt.gcf())