# Modules
import altair as alt
import streamlit as st
import requests
import pandas as pd

# INSERT YOUR API  KEY WHICH YOU PASTED IN YOUR secrets.toml file
api_key = st.secrets["api_key"]

url_1 = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid={}'
url_2 = 'https://api.openweathermap.org/data/2.5/forecast?lat={}&lon={}&appid={}'

# Function for LATEST WEATHER DATA
def getweather(city):
    result = requests.get(url_1.format(city, api_key))
    if result:
        json = result.json()
        country = json['sys']['country']
        temp = json['main']['temp'] - 273.15
        temp_feels = json['main']['feels_like'] - 273.15
        humid = json['main']['humidity']
        icon = json['weather'][0]['icon']
        lon = json['coord']['lon']
        lat = json['coord']['lat']
        des = json['weather'][0]['description']
        res = [country, round(temp, 1), round(temp_feels, 1),
               humid, lon, lat, icon, des]
        return res, json
    else:
        print("error in search !")

# Function for MAX TEMPERATURE
def get_maxtemp_forecast_data(lat,lon):
    result = requests.get(url_2.format(lat, lon, api_key))
    if result:
        data = result.json()
        temp_max = []
        date = []
        for main in data["list"]:
            t = main["main"]["temp_max"]
            temp_max.append(t - 273.5)
            d = main["dt_txt"]
            date.append(d)
        return data , temp_max, date
    
# Function for HUMIDITY
def get_humidity(lat,lon):
    result = requests.get(url_2.format(lat, lon, api_key))
    if result:
        data = result.json()
        hum = []
        date = []        
        for main in data["list"]:
            h = main["main"]["humidity"]
            hum.append(h)
            d = main["dt_txt"]
            date.append(d)
        return data , hum , date 

# Let's write the Application

st.markdown("<h1 style='text-align: center; color: gray;'>Streamlit Weather Report</h1>", unsafe_allow_html=True)

page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] > .main {{
background-image: url("https://assets.wfcdn.com/im/13048039/resize-h445%5Ecompr-r85/1599/159936424/Tiny+Tots+2+Wallpaper.jpg");
background-size: cover;
background-position: center center;
background-repeat: no-repeat;
background-attachment: local;
}}
</style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)

weather = st.select_slider(
    'What type of weather is your favorite?',
    options=['Sunny','Cloudy','Snow','Rain'])
if weather == 'Snow':
    image0 = 'snowing.gif'
    st.image(image0, use_column_width=True, caption='Somewhere in the World.')
elif weather == 'Cloudy':
    image1 = 'cloudy.gif'
    st.image(image1, use_column_width=True, caption='Somwhere in the World.')
elif weather == 'Sunny':
    image2 = 'sunny.gif'
    st.image(image2, use_column_width=True, caption='Somwhere in the World.')
elif weather == 'Rain':
    image3 = 'rainy.gif'
    st.image(image3, use_column_width=True, caption='Somwhere in the World.')

col1, col2 = st.columns(2)

with col1:
    city_name = st.text_input("Enter a city name")
    show_forecast_data = st.button('5 Day/3 Hour Forecast')
    show_map = st.checkbox('Show map')
try:
    with col2:
        if city_name:
            res, json = getweather(city_name)
            st.markdown('''
            <style>
            .element-container {
                opacity: 1;
            }
            </style>
            ''', unsafe_allow_html=True)
            st.success('Current: ' + str(round(res[1], 2)) + ' C°')
            st.info('Feels Like: ' + str(round(res[2], 2)) + ' C°')
            st.info('Humidity: ' + str(round(res[3], 2)) + ' %')
            st.subheader('Status: ' + res[7])
            web_str = "![Alt Text]" + "(http://openweathermap.org/img/wn/" + str(res[6]) + "@2x.png)"
            st.markdown(web_str)

    if city_name and show_forecast_data:
        res, json = getweather(city_name)
        data, tempMax, date = get_maxtemp_forecast_data(res[5], res[4])

        chart_data = pd.DataFrame({
            'Temperature in Celsius': tempMax,
            'Date': date
        })
        bar_chart = alt.Chart(chart_data, title = "Daily Max Temperature").mark_bar().encode(
            y='Temperature in Celsius',
            x='Date',
        )
    
        data, humid, date = get_humidity(res[5], res[4])
        chart_data2 = pd.DataFrame({
            'Humidity': humid,
            'Date': date,
        })
        line_chart = alt.Chart(chart_data2, title = "Daily Humidity").mark_line().encode(
            y='Humidity',
            x='Date',
        ).interactive()

        tab1, tab2 = st.tabs(["5 Day/3 Hour Max Temperature Forecast","5 Day/3 Hour Humidity Forecast"])
        with tab1:
            st.altair_chart(bar_chart, use_container_width=True)
        with tab2:
            st.altair_chart(line_chart, use_container_width=True)

    if city_name and show_map:
        st.map(pd.DataFrame({'lat': [res[5]], 'lon': [res[4]]}, columns=['lat', 'lon']))
except:
    st.error('There is no city by that name! Please re-enter the city name.')
