# Modules
import altair as alt
import streamlit as st
import requests
import pandas as pd
import base64

# INSERT YOUR API  KEY WHICH YOU PASTED IN YOUR secrets.toml file
api_key = st.secrets["api_key"]

url_1 = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid={}'
url_2 = 'https://api.openweathermap.org/data/2.5/forecast?lat={}&lon={}&appid={}'

@st.cache_data
def get_img_as_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Function for LATEST WEATHER DATA
def getweather(city):
    result = requests.get(url_1.format(city, api_key))
    if result:
        json = result.json()
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

# Let's write the Application

st.markdown("<h1 style='text-align: center; color: gray;'>Streamlit Weather Report</h1>", unsafe_allow_html=True)

page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] > .main {{
background-image: url("https://img.freepik.com/free-vector/blue-sky-with-shiny-clouds-background_1017-23279.jpg?w=826&t=st=1689355159~exp=1689355759~hmac=14743d9b91587e62cace25a8a84e39e997e42bb12fb8549b91d56613b7a04758");
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
    show_forecast_data = st.button('5 Day/3 Hour Max Temp Forecast')
    show_map = st.checkbox('Show map')
with col2:
    if city_name:
        res, json = getweather(city_name)
        st.success('Current: ' + str(round(res[1], 2)) + ' C°')
        st.info('Feels Like: ' + str(round(res[2], 2)) + ' C°')
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
