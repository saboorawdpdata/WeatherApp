import streamlit as st
import requests
import json
from datetime import datetime
 

st.set_page_config(
    page_title="My Weather App",
    page_icon="🌤️",
    layout="centered"
)

st.title("🌤️ My Weather App")

#sidebar

with st.sidebar:
    st.header("Settings")

    api_key=st.text_input("Enter API KEY:",placeholder="Enter your API KEY HERE")

col1,col2=st.columns([3,1])

with col1:
    city=st.text_input("Enter city name:",placeholder="eg: lahore, london etc.",value="Karachi")

with col2:
    units=st.selectbox("Units:",options=["Centigrade","Farhenheit"],index=0)    

unit_param="metric" if units=="Centigrade" else "Farhenheit"  

    #search button
search_btn=st.button("Get Weather",type="primary", use_container_width=True)

    #function to fetch weather data
def get_weather(city_name,api_key,unit_system):
    base_url="https://api.openweathermap.org/data/2.5/weather"
        
    params={"q":city_name,"appid":api_key,"units":unit_system}
        
    try:
        response=requests.get(base_url,params=params,timeout=10)

        if response.status_code==200:
            return response.json(),None
        elif response.status_code==401:
            return None,"Invalid API KEY"
        elif response.status_code==404:
            return None, "Invalid City Name! city {city_name} Not Found!"
        else:
            return None, "Error in API or Format!"
    except response.exceptions.ConnectionError:
        return None, "No Internet conncection!"
    except response.exceptions.Timeout:
        return None, "Request Time Out Error!"
    except Exception as e:
        return None, f"An Error Occurred:{str(e)}"

if search_btn:
    if not api_key:
        st.warning("Please Enter Your API Key in the sidebar!")
    elif not city.strip():
        st.warning("Please Enter City Name!")
    else:
        with st.spinner(f"Fething Weather Data for your city that is {city}..."):
            weather_data,error_msg=get_weather(city.strip(),api_key,unit_param)

        if error_msg:
            st.error(error_msg) 
        else:
            st.success(f"Weather Data Fetched Successfully!") 

            #extract Data
            temp=weather_data['main']['temp']
            humidity=weather_data['main']['humidity']
            feels_like=weather_data['main']['feels_like']
            pressure=weather_data['main']['pressure']
            

            weather_desc=weather_data['weather'][0]['description'].title()
            weather_icon=weather_data['weather'][0]['icon']

            #wind_speed=weather_data['weather']['speed']
            #wind_deg=weather_data['wind'].get('deg',0)


            city_name=weather_data['name']
            country=weather_data['sys']['country']

            #main weather info

            col1,col2,col3=st.columns([2,1,1])

            with col1:
                st.markdown(f"### {temp} {'C' if unit_param =='metric' else 'F'}")
                st.markdown(f"**** Feels like:*** {feels_like} {'C' if unit_param=='metric' else 'F'}")
                st.markdown(f"***{weather_desc}***")

            with col2:
                icon_url=f"https://openweathermap.org/img/wn/{weather_icon}@2x.png"
                st.image(icon_url,width=100)

            with col3:
                st.metric("Humidity", f"{humidity}%")   

            # Additional Details 
            col1,col2,col3,col4 = st.columns(4)

            #with col1:
               # st.metric("Wind Speed", f"{wind_speed} m/s") 
            with col1:
                clouds=weather_data.get('clouds',{}).get('all','N/A')
                st.metric("Cloud Cover", f"{clouds}%")
                      
            st.markdown("-------------") 
            st.caption(f"Data Provided by OpenWeatherMap | Last Updated: {datetime.now().strftime('%H:%M:%S')}")         


          
                            

