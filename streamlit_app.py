import streamlit as st
import requests
import json
import pandas as pd
import altair as alt

# --- API Key ---
API_KEY = "df7ead2b880e18ef32c2e0d12d4c50fcbb505dc4"

def get_air_quality(city_name, api_key=API_KEY):
    """Fetches air quality data for a given city using the WAQI API."""
    base_url = "https://api.waqi.info/feed/"
    url = f"{base_url}{city_name}/?token={api_key}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes
        data = response.json()
        if data["status"] == "ok":
            aqi = data["data"]["aqi"]
            temperature = None
            dominant_pollutant_name = None
            dominant_pollutant_value = None

            if "iaqi" in data["data"]:
                if "t" in data["data"]["iaqi"] and "v" in data["data"]["iaqi"]["t"]:
                    temperature = data["data"]["iaqi"]["t"]["v"]

                potential_pollutants = ["pm25", "pm10", "o3", "no2", "co", "so2"]
                for pollutant_key in potential_pollutants:
                    if pollutant_key in data["data"]["iaqi"] and "v" in data["data"]["iaqi"][pollutant_key]:
                        dominant_pollutant_name = pollutant_key.upper()
                        dominant_pollutant_value = data["data"]["iaqi"][pollutant_key]["v"]
                        break

                if "dominantpol" in data["data"]:
                    dominant_pollutant_name = data["data"]["dominantpol"].upper()
                    # You might need to fetch the value separately based on the API response

            return aqi, temperature, dominant_pollutant_name, dominant_pollutant_value
        else:
            st.error(f"Error fetching data for {city_name}: {data['message']}")
            return None, None, None, None
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to API for {city_name}: {e}")
        return None, None, None, None
    except json.JSONDecodeError as e:
        st.error(f"Error decoding JSON for {city_name}: {e}")
        return None, None, None, None

def get_aqi_category(aqi):
    """Categorizes AQI value into descriptive terms and colors."""
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

st.set_page_config(page_title="EnviroBot", layout="wide")

# --- Background Image ---
def set_background(image_url):
    """Sets the background image of the Streamlit app."""
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("{image_url}");
            background-attachment: fixed;
            background-size: cover;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

background_image_url = "https://images.unsplash.com/photo-1552733407-5d5c46c3bb03?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxzZWFyY2h8MTd8fGJsYW5rfGVufDB8fDB8fA%3D%3D&auto=format&fit=crop&w=800&q=60" # Replace with your image URL
set_background(background_image_url)

# --- Sidebar for Navigation ---
with st.sidebar:
    st.title("EnviroBot")
    locations = ["Dubai", "Delhi", "London", "Beijing", "New York"]
    selected_location_sidebar = st.selectbox("Choose a City:", [""] + locations, key="location_select_sidebar")

    st.markdown("---")
    st.subheader("Chatbot")
    st.markdown("*Under Development*")

    st.markdown("---")
    if st.button("More Cities"):
        st.session_state["show_more_cities"] = True
    if st.session_state.get("show_more_cities"):
        additional_city = st.text_input("Enter city name:")
        if st.button("Add City") and additional_city:
            if additional_city.strip().capitalize() not in locations:
                locations.append(additional_city.strip().capitalize())
                st.session_state["show_more_cities"] = False
                st.rerun()
            else:
                st.warning("City already in the list.")
        if st.button("Hide"):
            st.session_state["show_more_cities"] = False
            st.rerun()

# --- Main Content Area ---
st.markdown(
    """
    <style>
    .title-container {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 80vh; /* Adjust as needed for vertical centering */
        background-color: rgba(0, 0, 0, 0.5); /* Semi-transparent black background */
        color: white; /* White text color */
        padding: 20px;
        border-radius: 10px; /* Optional rounded corners */
        text-align: center; /* Center the text within the container */
    }
    .by-rohit {
        position: fixed;
        bottom: 10px;
        right: 10px;
        font-size: 0.8em;
        color: white; /* White text color */
        background-color: rgba(0, 0, 0, 0.5); /* Semi-transparent black background */
        padding: 5px;
        border-radius: 5px; /* Optional rounded corners */
    }
    </style>
    """,
    unsafe_allow_html=True,
)

if not st.session_state.get("location_selected"):
    st.markdown('<div class="title-container"><h1>EnviroBot</h1></div>', unsafe_allow_html=True)
    st.markdown('<div class="by-rohit">By Rohit</div>', unsafe_allow_html=True)
else:
    st.subheader(f"Real-time Air Quality in {st.session_state.selected_location}")
    city_param = st.session_state.selected_location.lower().replace(" ", "-")
    aqi, temp, pollutant_name, pollutant_value = get_air_quality(city_param)

    if aqi is not None:
        category, color = get_aqi_category(aqi)
        st.metric(label="AQI", value=aqi)
        st.markdown(f"<span style='color: {color}; font-size: 0.9em;'>{category}</span>", unsafe_allow_html=True)
        if temp is not None:
            st.metric("Temperature (°C)", value=temp)
        if pollutant_name:
            if pollutant_value is not None:
                st.caption(f"Dominant Pollutant: {pollutant_name} ({pollutant_value:.2f})")
            else:
                st.caption(f"Dominant Pollutant: {pollutant_name}")
    else:
        st.error(f"Could not retrieve current data for {st.session_state.selected_location}.")

# --- Update session state when a location is selected ---
if st.sidebar.selectbox("Choose a City:", [""] + locations, key="location_select_sidebar"):
    st.session_state["location_selected"] = True
    st.session_state["selected_location"] = st.session_state.location_select_sidebar
    st.rerun()
elif "location_selected" in st.session_state and st.session_state["selected_location"] == "":
    del st.session_state["location_selected"]
    st.rerun()
