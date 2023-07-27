# Modules
import altair as alt
import streamlit as st
import requests
import pandas as pd
import base64
import datetime

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
def get_maxtemp_forecast_data(lat, lon):
    result = requests.get(url_2.format(lat, lon, api_key))
    if result:
        data = result.json()
        temp_max = []
        date = []
        if measurements == "Metric":
            for main in data["list"]:
                t = main["main"]["temp_max"]
                temp_max.append(t - 273.5)
                d = main["dt_txt"]
                date.append(d)
            return data, temp_max, date
        else:
            for main in data["list"]:
                t = main["main"]["temp_max"]
                temp_max.append((t - 273.5) * 1.8 + 32)
                d = main["dt_txt"]
                date.append(d)
            return data, temp_max, date


# Function for HUMIDITY
def get_humidity(lat, lon):
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
        return data, hum, date


# Function for AIR QUALITY
def get_air_quality(lat, lon):
    url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={api_key}"
    response = requests.get(url)
    if response:
        data = response.json()
        if data and 'list' in data:
            return data['list'][0]
    return None


# Function for HISTORICAL AIR QUALITY
def get_air_quality_history(lat, lon, start, end):
    url = f"http://api.openweathermap.org/data/2.5/air_pollution/history?lat={lat}&lon={lon}&start={start}&end={end}&appid={api_key}"
    response = requests.get(url)
    if response:
        data = response.json()
        if data and 'list' in data:
            return data['list'][0]
    return None


def get_weather_by_time(city, input_time):
    result = requests.get(url_1.format(city, api_key))
    if result:
        json = result.json()
        lon = json['coord']['lon']
        lat = json['coord']['lat']
        forecast_result = requests.get(url_2.format(lat, lon, api_key))
        if forecast_result:
            forecast_json = forecast_result.json()
            date_time_str = datetime.datetime.now().strftime('%Y-%m-%d') + " " + input_time.strftime('%H:%M:%S')
            selected_time = datetime.datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S')
            nearest_forecast = min(forecast_json['list'], key=lambda x: abs(
                datetime.datetime.strptime(x['dt_txt'], '%Y-%m-%d %H:%M:%S') - selected_time))
            country = json['sys']['country']
            temp = nearest_forecast['main']['temp'] - 273.15
            temp_feels = nearest_forecast['main']['feels_like'] - 273.15
            humid = nearest_forecast['main']['humidity']
            icon = nearest_forecast['weather'][0]['icon']
            des = nearest_forecast['weather'][0]['description']
            res = [country, round(temp, 1), round(temp_feels, 1),
                   humid, lon, lat, icon, des]
            return res, json
    else:
        print("error in search !")


# Let's write the Application

st.markdown("<h1 style='text-align: center; color: dark-gray;'>Weather Report 🌦️</h1>", unsafe_allow_html=True)


bgcolor = st.color_picker('Customize your background color', '#FFFFFF')
page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] > .main {{
background-color: {bgcolor}
}}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)
# else:
#     page_bg_img = f"""
#     <style>
#     [data-testid="stAppViewContainer"] > .main {{
#     background-image: url("https://assets.wfcdn.com/im/13048039/resize-h445%5Ecompr-r85/1599/159936424/Tiny+Tots+2+Wallpaper.jpg");
#     background-size: cover;
#     background-position: center center;
#     background-repeat: no-repeat;
#     background-attachment: local;
#     }}
#     </style>
#     """
# st.markdown(page_bg_img, unsafe_allow_html=True)


# weather = st.select_slider(
#     'What type of weather is your favorite?',
#     options=['Sunny', 'Cloudy', 'Snow', 'Rain'])
# if weather == 'Snow':
#     image0 = 'snowing.gif'
#     st.image(image0, use_column_width=True, caption='Somewhere in the World.')
# elif weather == 'Cloudy':
#     image1 = 'cloudy.gif'
#     st.image(image1, use_column_width=True, caption='Somewhere in the World.')
# elif weather == 'Sunny':
#     image2 = 'sunny.gif'
#     st.image(image2, use_column_width=True, caption='Somewhere in the World.')
# elif weather == 'Rain':
#     image3 = 'rainy.gif'
#     st.image(image3, use_column_width=True, caption='Somewhere in the World.')


def get_image_base64(image_path):
    with open(image_path, 'rb') as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')


weather = st.select_slider(
    'What type of weather is your favorite?',
    options=['Sunny ☀️', 'Cloudy ☁️', 'Snowy ❄️', 'Rainy ⛈️'])

if weather == 'Snowy ❄️':
    image_base64 = get_image_base64('snowing.gif')
    st.markdown(f"""
        <div style='border-radius: 35px; overflow: hidden;'>
            <img src='data:image/gif;base64,{image_base64}' width='100%' height='auto'/>
        </div>
        <div style='text-align: center;'>Somewhere in the World.   &#127757</div>
        """, unsafe_allow_html=True)
elif weather == 'Cloudy ☁️':
    image_base64 = get_image_base64('cloudy.gif')
    st.markdown(f"""
        <div style='border-radius: 35px; overflow: hidden;'>
            <img src='data:image/gif;base64,{image_base64}' width='100%' height='auto'/>
        </div>
        <div style='text-align: center;'>Somewhere in the World.   &#127757</div>
        """, unsafe_allow_html=True)
elif weather == 'Sunny ☀️':
    image_base64 = get_image_base64('sunny.gif')
    st.markdown(f"""
        <div style='border-radius: 35px; overflow: hidden;'>
            <img src='data:image/gif;base64,{image_base64}' width='100%' height='auto'/>
        </div>
        <div style='text-align: center;'>Somewhere in the World.   &#127757</div>
        """, unsafe_allow_html=True)
elif weather == 'Rainy ⛈️':
    image_base64 = get_image_base64('rainy.gif')
    st.markdown(f"""
        <div style='border-radius: 35px; overflow: hidden;'>
            <img src='data:image/gif;base64,{image_base64}' width='100%' height='auto'/>
        </div>
        <div style='text-align: center;'>Somewhere in the World.   &#127757</div>
        """, unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    city_name = st.text_input("Enter a city name")
    show_forecast_data = st.button('5 Day/3 Hour Forecast')
    show_map = st.checkbox('Show map')
    measurements = st.radio(
        "Measurement preference?",
        ["Metric", "Imperial"],
    )
try:
    with col2:
        if city_name:
            current_time = datetime.datetime.now().time()
            input_time = st.time_input('Enter a time', value=current_time)  # Setting default value as current time
            res, json = getweather(city_name)

            # Input for time

            if input_time:
                res, json = get_weather_by_time(city_name, input_time)
            else:
                res, json = getweather(city_name)

            # Fetching air quality data
            air_quality = None
            if input_time:
                from datetime import datetime, timedelta

                input_datetime = datetime.combine(datetime.today(), input_time)
                end = int(datetime.timestamp(input_datetime))
                start = end - 3600  # start is 1 hour before the end
                air_quality = get_air_quality_history(res[4], res[5], start, end)
            else:
                air_quality = get_air_quality(res[4], res[5])

            st.markdown('''
            <style>
            .element-container {
                opacity: 1;
            }
            </style>
            ''', unsafe_allow_html=True)

            if measurements == "Metric":
                st.success('Current: ' + str(round(res[1], 2)) + ' C°')
                st.success('Feels Like: ' + str(round(res[2], 2)) + ' C°')
                st.success('Humidity: ' + str(round(res[3], 2)) + ' %')
                st.subheader('Status: ' + res[7])
                web_str = "![Alt Text]" + "(http://openweathermap.org/img/wn/" + str(res[6]) + "@2x.png)"
                st.markdown(web_str)
            else:
                st.success('Current: ' + str(round(res[1] * 1.8 + 32, 2)) + ' F°')
                st.success('Feels Like: ' + str(round(res[2] * 1.8 + 32, 2)) + ' F°')
                st.success('Humidity: ' + str(round(res[3], 2)) + ' %')
                st.subheader('Status: ' + res[7])
                web_str = "![Alt Text]" + "(http://openweathermap.org/img/wn/" + str(res[6]) + "@2x.png)"
                st.markdown(web_str)

            # Prepare a summary of air quality
            aqi = air_quality['main']['aqi'] if air_quality else None
            air_quality_summary = 'Unknown 😷'
            if aqi is not None:
                if aqi == 1:
                    air_quality_summary = 'Good 😊'
                elif aqi == 2:
                    air_quality_summary = 'Fair 😐'
                elif aqi == 3:
                    air_quality_summary = 'Moderate 😷'
                elif aqi == 4:
                    air_quality_summary = 'Poor 🤒'
                elif aqi == 5:
                    air_quality_summary = 'Very Poor 🚫'

            # Display the summary of air quality
            st.markdown(f'**Air Quality:** {air_quality_summary}')

            # A button to show detailed air quality data
            if st.button('Show Detailed Air Quality'):
                # Prepare a DataFrame for air quality data
                air_quality_df = pd.DataFrame(air_quality['components'], index=[0])
                # Display the DataFrame
                st.table(air_quality_df)

    if city_name and show_forecast_data:
        res, json = getweather(city_name)
        data, tempMax, date = get_maxtemp_forecast_data(res[5], res[4])
        if measurements == "Metric":
            chart_data = pd.DataFrame({
                'Temperature in Celsius': tempMax,
                'Date': date
            })
            line_chart = alt.Chart(chart_data, title="Daily Max Temperature").mark_line().encode(
                y='Temperature in Celsius',
                x='Date',
            )
        else:
            chart_data = pd.DataFrame({
                'Temperature in Farenheit': tempMax,
                'Date': date
            })
            line_chart = alt.Chart(chart_data, title="Daily Max Temperature").mark_line().encode(
                y='Temperature in Farenheit',
                x='Date',
            )

        data, humid, date = get_humidity(res[5], res[4])
        chart_data2 = pd.DataFrame({
            'Humidity': humid,
            'Date': date,
        })
        bar_chart = alt.Chart(chart_data2, title="Daily Humidity").mark_bar().encode(
            y='Humidity',
            x='Date',
        ).interactive()

        tab1, tab2 = st.tabs(["5 Day/3 Hour Max Temperature Forecast", "5 Day/3 Hour Humidity Forecast"])
        with tab1:
            st.altair_chart(line_chart, use_container_width=False)
            if measurements == "Metric":
                st.dataframe(
                    chart_data[['Date', 'Temperature in Celsius']].set_index(chart_data.columns[1]).style.highlight_max(
                        axis=0), use_container_width=True)
            else:
                st.dataframe(chart_data[['Date', 'Temperature in Farenheit']].set_index(
                    chart_data.columns[1]).style.highlight_max(axis=0), use_container_width=True)
        with tab2:
            st.altair_chart(bar_chart, use_container_width=False)
            st.dataframe(chart_data2[['Date', 'Humidity']].set_index(chart_data.columns[1]).style.highlight_max(axis=0),
                         use_container_width=True)
    elif not city_name and show_forecast_data:
        st.error('A city name has not been entered! Please enter a city name.')

    if city_name and show_map:
        st.map(pd.DataFrame({'lat': [res[5]], 'lon': [res[4]]}, columns=['lat', 'lon']))
    elif not city_name and show_map:
        st.error('A city name has not been entered! Please enter a city name.')

except:
    st.error('There is no city by that name! Please re-enter the city name.')
