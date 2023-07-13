# Modules
import altair as alt
import streamlit as st
import requests
import pandas as pd

# INSERT YOUR API  KEY WHICH YOU PASTED IN YOUR secrets.toml file
api_key = st.secrets["api_key"]

url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid={}'
url_1 = 'https://api.openweathermap.org/data/2.5/forecast?lat={}&lon={}&appid={}'

# Function for LATEST WEATHER DATA
def getweather(city):
    result = requests.get(url.format(city, api_key))
    if result:
        json = result.json()
        # st.write(json)
        country = json['sys']['country']
        temp = json['main']['temp'] - 273.15
        temp_feels = json['main']['feels_like'] - 273.15
        humid = json['main']['humidity'] - 273.15
        icon = json['weather'][0]['icon']
        lon = json['coord']['lon']
        lat = json['coord']['lat']
        des = json['weather'][0]['description']
        res = [country, round(temp, 1), round(temp_feels, 1),
               humid, lon, lat, icon, des]
        return res, json
    else:
        print("error in search !")

# Function for HISTORICAL DATA
def get_forecast_data(lat,lon):
    res = requests.get(url_1.format(lat, lon, api_key))
    data = res.json()
    temp_max = []
    date = []
    for main in data["list"]:
        t = main["main"]["temp_max"]
        temp_max.append(t - 273.5)
        d = main["dt_txt"]
        date.append(d)
    return data , temp_max, date

# Let's write the Application

st.header('Streamlit Weather Report')
st.markdown('https://openweathermap.org/api')

im1, im2 = st.columns(2)
with im2:
    image0 = 'iceland.jpeg'
    st.image(image0, use_column_width=True, caption='Somewhere in The Netherlands.')
with im1:
    image1 = 'open weather map.png'
    st.image(image1, caption='We will use Open Weather Map API as our Data Resource.', use_column_width=True)

col1, col2 = st.columns(2)

with col1:
    city_name = st.text_input("Enter a city name")
    show_forecast_data = st.button('5 Day/3 Hour Max Temp Forecast')
    show_map = st.checkbox('Show map')
with col2:
    if city_name:
        res, json = getweather(city_name)
        st.success('Current: ' + str(round(res[1], 2)))
        st.info('Feels Like: ' + str(round(res[2], 2)))
        st.subheader('Status: ' + res[7])
        web_str = "![Alt Text]" + "(http://openweathermap.org/img/wn/" + str(res[6]) + "@2x.png)"
        st.markdown(web_str)

if city_name and show_forecast_data:
    res, json = getweather(city_name)
    data, tempMax, date = get_forecast_data(res[5], res[4])

    "5 Day/3 Hour Forecast (Max Temperature)"
    chart_data = pd.DataFrame({
        'Temperature in Celsius': tempMax,
        'Date': date
    })
    bar_chart = alt.Chart(chart_data).mark_bar().encode(
        y='Temperature in Celsius',
        x='Date',
    )
    st.altair_chart(bar_chart, use_container_width=True)

if city_name and show_map:
    st.map(pd.DataFrame({'lat': [res[5]], 'lon': [res[4]]}, columns=['lat', 'lon']))

