import streamlit as st
import requests
import json

def get_air_quality(city_name, api_key="df7ead2b880e18ef32c2e0d12d4c50fcbb505dc4"):
    base_url = "https://api.waqi.info/feed/"
    url = f"{base_url}{city_name}/?token={api_key}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if data["status"] == "ok":
            aqi = data["data"]["aqi"]
            temperature = None
            if "iaqi" in data["data"] and "t" in data["data"]["iaqi"]:
                temperature = data["data"]["iaqi"]["t"]["v"]
            return aqi, temperature
        else:
            st.error(f"Error fetching data for {city_name}: {data['message']}")
            return None, None
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to API for {city_name}: {e}")
        return None, None
    except json.JSONDecodeError as e:
        st.error(f"Error decoding JSON for {city_name}: {e}")
        return None, None

st.set_page_config(page_title="Air Quality Comparison", layout="centered")
st.title("Air Quality in Dubai vs. Delhi")
st.markdown("Comparing real-time Air Quality Index (AQI) and temperature.")

dubai_aqi, dubai_temp = get_air_quality("dubai")
delhi_aqi, delhi_temp = get_air_quality("delhi")

st.subheader("Current Air Quality:")

st.markdown("### Dubai")
if dubai_aqi is not None:
    st.metric("AQI", value=dubai_aqi)
else:
    st.error("Could not retrieve current AQI for Dubai.")
if dubai_temp is not None:
    st.metric("Temperature (°C)", value=dubai_temp)
else:
    st.warning("Temperature data not currently available for Dubai.")

st.markdown("### Delhi")
if delhi_aqi is not None:
    st.metric("AQI", value=delhi_aqi)
else:
    st.error("Could not retrieve current AQI for Delhi.")
if delhi_temp is not None:
    st.metric("Temperature (°C)", value=delhi_temp)
else:
    st.warning("Temperature data not currently available for Delhi.")

st.subheader("Comparison:")

if dubai_aqi is not None and delhi_aqi is not None:
    if dubai_aqi < delhi_aqi:
        st.success("The air quality in Dubai is currently better than in Delhi.")
    elif delhi_aqi < dubai_aqi:
        st.warning("The air quality in Delhi is currently worse than in Dubai.")
    else:
        st.info("The air quality in Dubai and Delhi is currently similar.")
else:
    st.info("Cannot compare AQI as data for one or both cities is unavailable.")

if dubai_temp is not None and delhi_temp is not None:
    if dubai_temp > delhi_temp:
        st.success("Dubai is currently warmer than Delhi.")
    elif delhi_temp > dubai_temp:
        st.info("Delhi is currently warmer than Dubai.")
    else:
        st.info("Dubai and Delhi have a similar temperature.")
else:
    st.info("Cannot compare temperature as data for one or both cities is unavailable.")
