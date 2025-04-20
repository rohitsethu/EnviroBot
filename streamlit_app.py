import streamlit as st
import requests
import json
import pandas as pd
import altair as alt


API_KEY = "df7ead2b880e18ef32c2e0d12d4c50fcbb505dc4"

def get_air_quality(city_name, api_key=API_KEY):
    base_url = "https://api.waqi.info/feed/"
    url = f"{base_url}{city_name}/?token={api_key}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if data["status"] == "ok":
            aqi = data["data"]["aqi"]
            temperature = None
            dominant_pollutant = None
            if "iaqi" in data["data"]:
                if "t" in data["data"]["iaqi"]:
                    temperature = data["data"]["iaqi"]["t"]["v"]
                if "p" in data["data"]["iaqi"]:
                    dominant_pollutant = data["data"]["iaqi"]["p"]["v"]
            return aqi, temperature, dominant_pollutant
        else:
            st.error(f"Error fetching data for {city_name}: {data['message']}")
            return None, None, None
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to API for {city_name}: {e}")
        return None, None, None
    except json.JSONDecodeError as e:
        st.error(f"Error decoding JSON for {city_name}: {e}")
        return None, None, None

def get_aqi_category(aqi):
    if aqi <= 50:
        return "Good", "green"
    elif aqi <= 100:
        return "Satisfactory", "lightgreen"
    elif aqi <= 200:
        return "Moderate", "yellow"
    elif aqi <= 300:
        return "Poor", "orange"
    elif aqi <= 400:
        return "Very Poor", "red"
    else:
        return "Severe", "darkred"

st.set_page_config(page_title="Air Quality Dashboard", layout="wide")
st.title("Air Quality Dashboard")

menu = ["Dubai", "Delhi", "Comparison", "More Locations", "AI Chat"]
choice = st.sidebar.selectbox("Navigation", menu)

if choice == "Dubai":
    st.subheader("🇦🇪 Real-time Air Quality in Dubai")
    aqi, temp, pollutant = get_air_quality("dubai")
    if aqi is not None:
        category, color = get_aqi_category(aqi)
        st.metric(label="AQI", value=aqi, delta=f"({category})", delta_color="normal")
        st.markdown(f"<span style='color: {color}; font-size: 0.9em;'>{category}</span>", unsafe_allow_html=True)
        if temp is not None:
            st.metric("Temperature (°C)", value=temp)
        if pollutant:
            st.caption(f"Dominant Pollutant: {pollutant}")
    else:
        st.error("Could not retrieve current data for Dubai.")

elif choice == "Delhi":
    st.subheader("🇮🇳 Real-time Air Quality in Delhi")
    aqi, temp, pollutant = get_air_quality("delhi")
    if aqi is not None:
        category, color = get_aqi_category(aqi)
        st.metric(label="AQI", value=aqi, delta=f"({category})", delta_color="normal")
        st.markdown(f"<span style='color: {color}; font-size: 0.9em;'>{category}</span>", unsafe_allow_html=True)
        if temp is not None:
            st.metric("Temperature (°C)", value=temp)
        if pollutant:
            st.caption(f"Dominant Pollutant: {pollutant}")
    else:
        st.error("Could not retrieve current data for Delhi.")

elif choice == "Comparison":
    st.subheader("Air Quality Comparison: Dubai vs. Delhi")
    dubai_col, delhi_col = st.columns(2)

    with dubai_col:
        st.markdown("### 🇦🇪 Dubai")
        dubai_aqi, dubai_temp, dubai_pollutant = get_air_quality("dubai")
        if dubai_aqi is not None:
            category, color = get_aqi_category(dubai_aqi)
            st.metric(label="AQI", value=dubai_aqi, delta=f"({category})", delta_color="normal")
            st.markdown(f"<span style='color: {color}; font-size: 0.9em;'>{category}</span>", unsafe_allow_html=True)
            if dubai_temp is not None:
                st.metric("Temperature (°C)", value=dubai_temp)
            if dubai_pollutant:
                st.caption(f"Dominant Pollutant: {dubai_pollutant}")
        else:
            st.error("Could not retrieve current data for Dubai.")

    with delhi_col:
        st.markdown("### 🇮🇳 Delhi")
        delhi_aqi, delhi_temp, delhi_pollutant = get_air_quality("delhi")
        if delhi_aqi is not None:
            category, color = get_aqi_category(delhi_aqi)
            st.metric(label="AQI", value=delhi_aqi, delta=f"({category})", delta_color="normal")
            st.markdown(f"<span style='color: {color}; font-size: 0.9em;'>{category}</span>", unsafe_allow_html=True)
            if delhi_temp is not None:
                st.metric("Temperature (°C)", value=delhi_temp)
            if delhi_pollutant:
                st.caption(f"Dominant Pollutant: {pollutant}")
        else:
            st.error("Could not retrieve current data for Delhi.")

    st.markdown("---")
    st.subheader("Comparison Insights:")
    if dubai_aqi is not None and delhi_aqi is not None:
        if dubai_aqi < delhi_aqi:
            st.success(f"The current AQI in Dubai ({dubai_aqi}) is better than in Delhi ({delhi_aqi}).")
        elif delhi_aqi < dubai_aqi:
            st.warning(f"The current AQI in Delhi ({delhi_aqi}) is worse than in Dubai ({dubai_aqi}).")
        else:
            st.info(f"The current AQI in Dubai ({dubai_aqi}) and Delhi ({delhi_aqi}) is similar.")
    else:
        st.info("Cannot compare AQI as data for one or both cities is unavailable.")

    if dubai_temp is not None and delhi_temp is not None:
        if dubai_temp > delhi_temp:
            st.success(f"Dubai is currently warmer ({dubai_temp}°C) than Delhi ({delhi_temp}°C).")
        elif delhi_temp > dubai_temp:
            st.info(f"Delhi is currently warmer ({delhi_temp}°C) than Dubai ({dubai_temp}°C).")
        else:
            st.info(f"Dubai and Delhi have a similar temperature ({dubai_temp}°C).")
    else:
        st.info("Cannot compare temperature as data for one or both cities is unavailable.")

elif choice == "More Locations":
    st.subheader("Explore Air Quality in Other Locations")
    location = st.text_input("Enter city name (e.g., London, Beijing):")
    if location:
        aqi, temp, pollutant = get_air_quality(location.lower().replace(" ", "-")) # API uses lowercase with hyphens
        st.markdown(f"### {location.capitalize()}")
        if aqi is not None:
            category, color = get_aqi_category(aqi)
            st.metric(label="AQI", value=aqi, delta=f"({category})", delta_color="normal")
            st.markdown(f"<span style='color: {color}; font-size: 0.9em;'>{category}</span>", unsafe_allow_html=True)
            if temp is not None:
                st.metric("Temperature (°C)", value=temp)
            if pollutant:
                st.caption(f"Dominant Pollutant: {pollutant}")
        else:
            st.error(f"Could not retrieve current data for {location}.")

elif choice == "AI Chat":
    st.subheader("AI Chatbot for Air Quality Info")
    st.markdown("This is a placeholder for a future AI chatbot.")
    st.markdown("You could integrate a language model here to answer questions about air quality, pollutants, health impacts, etc.")
    st.markdown("*(AI chatbot functionality needs further implementation.)*")
