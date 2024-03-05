import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
sns.set(style='dark')

# read day data dan hour data
day_df = pd.read_csv('day.csv')
hour_df = pd.read_csv('hour.csv')

# menghapus kolom yang tidak digunakan atau tidak berhubungan dengan pertanyaan
drop_columns = ['season','holiday','weekday','workingday','temp','atemp','hum','windspeed']
for column in drop_columns:
        day_df.drop(labels = column, axis=1, inplace=True)
        hour_df.drop(labels = column, axis=1, inplace=True)

# mengubah tipe data dteday menjadi datetime
day_df['dteday'] = pd.to_datetime(day_df['dteday'])
hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])

# mengubah nama kolom pada tabel day_df
day_df.rename(columns={
    'dteday':'date', 'yr':'year', 'weathersit':'weather',
    'mnth':'month','cnt':'count'
}, inplace=True)

# mengubah nama kolom pada tabel hour_df
hour_df.rename(columns={
    'dteday':'date', 'yr':'year', 'weathersit':'weather',
    'mnth':'month', 'hr':'hour', 'cnt':'count'
}, inplace=True)

# Mengkonversi nilai-nilai pada kolom tabel tertentu menjadi kategorik pada tabel day_df
month_dict = {
    1:'January', 2:'February', 3:'March', 4:'April', 5:'May', 6:'June',
    7:'July', 8:'August', 9:'September', 10:'October', 11:'November', 12:'December'
}

wheather_dict = {
    1:'Clear', 2:'Mist/Cloudy',
    3:'Light Rain/Snow', 4:'Heavy Rain/snow'
}

year_dict = {
    0:2011, 1:2012
}

day_df["month"] = day_df["month"].map(lambda x: month_dict[x])
day_df["weather"] = day_df["weather"].map(lambda x: wheather_dict[x])
day_df["year"] = day_df["year"].map(lambda x: year_dict[x])

# Mengkonversi nilai-nilai pada kolom tabel tertentu menjadi kategorik pada tabel hour_df
hour_df["month"] = hour_df["month"].map(lambda x: month_dict[x])
hour_df["weather"] = hour_df["weather"].map(lambda x: wheather_dict[x])
hour_df["year"] = hour_df["year"].map(lambda x: year_dict[x])

# Menambah keterangan waktu 
hour_df['time'] = hour_df['hour'].apply(lambda x: "Night" if (x < 5 or x >= 18) else("Morning" if (x >= 5 and x < 12) else "Afternoon"))

# Mengubah format hour menjadi am-pm
hour_df['hour'] = hour_df['hour'].apply(lambda x: str(x)+" am" if x < 12 else str(x-12)+" pm")

# Kumpulan function
def monthly_stats(df):
    monthly_count = df.groupby(by=['year','month']).agg({
                "count": "sum"}).reset_index()

    monthly_count['month'] = pd.Categorical(monthly_count['month'], categories=
        ['January','February','March','April','May','June','July','August',
        'September','October','November','December'],ordered=True)
    return monthly_count

def times_stats(df):
    time_count = df.groupby(by='time').agg({
            'count':'sum'}).reset_index()

    time_count['time'] = pd.Categorical(time_count['time'], 
                                     categories=['Morning', 'Afternoon', 'Night'], ordered=True)
    
    return time_count

def weather_stats(df):
    weather_count = df.groupby(by='weather').agg({'count':'sum'}).reset_index()   

    return weather_count  

def year_result(df):
    yearly = df.groupby(by='year').agg({'casual':['sum','mean'],
                               'registered':['sum', 'mean'],'count':['min', 'max', 'sum', 'mean']})
    return yearly

def month_result(df):
     monthly = df.groupby(by='month').agg({'casual':['sum','mean'],
                                 'registered':['sum', 'mean'],'count':['min','max','sum','mean']})
     return monthly

def weather_result(df):
     weatherly = df.groupby(by='weather').agg({'casual':['min','max','sum','mean'],
                                                    'registered':['min','max','sum','mean'],'count':['sum','mean']})
     return weatherly

def time_result(df):
     timely = df.groupby(by='time').agg({'casual':['min','max','sum','mean'],
                                              'registered':['min','max','sum','mean'],'count':['sum','mean']})
     return timely

with st.sidebar:
    #  st.image('https://github.com/Arrizalibnu/Bike-Sharing-Analys/blob/main/bike.png')
     st.header('Lets Bike!')

st.title('Bike Sharing Analysis 2011-2012 Dashboard')
tab1, tab2, tab3 = st.tabs(["Tab 1", "Tab 2", "Tab 3"])

month = monthly_stats(day_df)
time = times_stats(hour_df)
weather = weather_stats(hour_df)

with tab1:
     fig = plt.figure(figsize=(18,8))
     plt.plot(day_df['date'], day_df['count'], color='blue')
     plt.title("Peforma Jasa sewa sepeda sepanjang tahun 2011 dan 2012", size=20, loc='center')
     plt.ylabel("Jumlah yang disewa")
     st.pyplot(fig)

     figs, ax = plt.subplots(nrows=1, ncols=2, figsize=(18,6))

     sns.barplot(x='count', y='month', data=month[month['year'] == 2011],
                 ax=ax[0])
     ax[0].set_ylabel(None)
     ax[0].set_xlabel('Jumlah sepeda disewa')
     ax[0].set_title("Peforma Jasa sewa sepeda tahun 2011", loc='center', fontsize=15)
     ax[0].tick_params(axis='y', labelsize=12)
     
     sns.barplot(x='count', y='month', data=month[month['year'] == 2012],
                 ax=ax[1])
     ax[1].set_xlabel('Jumlah sepeda disewa')
     ax[1].set_ylabel(None)
     ax[1].set_title("Peforma Jasa sewa sepeda tahun 2012", loc='center', fontsize=15)
     ax[1].tick_params(axis='y', labelsize=12)
     st.pyplot(figs)
     st.caption('Berdasarkan grafik peforma jasa sewa sepeda sepanjang tahun 2011 dan 2012 terdapat adanya peningkatan sepeda disewa pada pertengahan tahun (Mei-Agustus). Hal ini diperkuat oleh grafik per bulan pada tahun 2011 dan 2012.')

with tab2:
     fig2 = plt.figure(figsize=(14,7))
     colors = ['#F0F8FF', '#FBCB78', '#191970']
     
     sns.barplot(y=time['count'], x=time['time'],orient='v')
     plt.xlabel(None)
     plt.ylabel("Jumlah sepeda disewa (Juta)")
     plt.title("Jumlah Sepeda disewa berdasarkan waktu")
     st.pyplot(fig2)
     st.caption('Pada waktu siang dan sore hari sepeda paling banyak disewa. Sedangkan pada waktu pagi hari ialah waktu paling sedikit sepeda disewa.')

with tab3:
     fig3 = plt.figure(figsize=(12,6))
     sns.barplot(x=weather['weather'], y=weather['count'], orient='v', errorbar=None)
     plt.xlabel(None)
     plt.ylabel("Jumlah sepeda disewa (Juta)")
     plt.title("Jumlah sepeda disewa berdasarkan cuaca")
     st.pyplot(fig3)
     st.caption('Terdapat pengaruh cuaca terhadap banyaknya sepeda yang disewa. Hal ini ditunjukkan bahwa pada cuaca cerah jauh lebih banyak sepeda yang disewa.')