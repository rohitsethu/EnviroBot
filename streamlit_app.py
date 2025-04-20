import streamlit as st
import pandas as pd
import numpy as np
import requests
import json

# --- Function to fetch current data from aqi.in API ---
def get_current_data_aqi_in(city_name="Dubai", api_key="df7ead2b880e18ef32c2e0d12d4c50fcbb505dc4"):
    base_url = "https://api.waqi.info/feed/"
    url = f"{base_url}{city_name}/?token={api_key}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes
        data = response.json()
        if data["status"] == "ok":
            aqi = data["data"]["aqi"]
            st.info(f"Raw AQI data from aqi.in: {data}") # For debugging
            current_temp = None
            if "iaqi" in data["data"] and "t" in data["data"]["iaqi"]:
                current_temp = data["data"]["iaqi"]["t"]["v"]

            # Placeholders for traffic and industry - aqi.in doesn't provide these
            current_traffic = 5
            current_industry = 5

            return np.array([[current_temp, current_traffic, current_industry]])
        else:
            st.error(f"Error fetching data from aqi.in: {data['message']}")
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to aqi.in API: {e}")
        return None
    except json.JSONDecodeError as e:
        st.error(f"Error decoding JSON response from aqi.in: {e}")
        return None

# --- Streamlit App ---
st.set_page_config(page_title="Real-time AI Air Pollution Predictor (Dubai)", layout="centered")
st.title("Real-time AI Air Pollution Predictor (Dubai)")
st.markdown("Predict AQI based on current temperature (from aqi.in) and placeholder values for traffic and industrial activity.")
st.markdown("This version does not use historical data for training.")

# --- Fetch current data from aqi.in and "predict" ---
st.sidebar.header("Current Conditions (Dubai)")
current_data = get_current_data_aqi_in(city_name="Dubai")

if current_data is not None:
    current_temp = current_data[0][0]
    placeholder_traffic = current_data[0][1]
    placeholder_industry = current_data[0][2]

    st.subheader("Current Conditions Retrieved from aqi.in:")
    if current_temp is not None:
        st.write(f"🌡️ Temperature: {current_temp}°C")
    else:
        st.warning("Temperature data not currently available from aqi.in.")
    st.write(f"🚗 Traffic Level (Placeholder): {placeholder_traffic} (Note: Real data not available from aqi.in)")
    st.write(f"🏭 Industrial Activity (Placeholder): {placeholder_industry} (Note: Real data not available from aqi.in)")

    # --- Since we don't have a trained model, we can only display the fetched AQI ---
    # --- You would need a pre-trained model or a different approach to make a prediction ---
    # --- based on temperature (if that's the only reliable real-time data you have) ---

    # Attempt to get the current AQI directly from the API response
    base_url = "https://api.waqi.info/feed/"
    api_key = "df7ead2b880e18ef32c2e0d12d4c50fcbb505dc4"
    url = f"{base_url}dubai/?token={api_key}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if data["status"] == "ok":
            current_aqi_from_api = data["data"]["aqi"]
            st.subheader("Current Air Quality Index (from aqi.in):")
            st.success(f" **{current_aqi_from_api} AQI**")
        else:
            st.error(f"Error fetching AQI from aqi.in: {data['message']}")
    except Exception as e:
        st.error(f"Error fetching AQI: {e}")

else:
    st.error("Failed to retrieve current data from aqi.in.")
