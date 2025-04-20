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

            # Placeholders for traffic and industry - you'll need to find
            # alternative data sources or methods if you want to include these
            current_traffic = st.session_state.get("current_traffic", 5)
            current_industry = st.session_state.get("current_industry", 5)

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

# --- Rest of your Streamlit code remains the same, but ensure you are calling this updated function ---
st.set_page_config(page_title="AI Air Pollution Predictor", layout="centered")
st.title("AI Air Pollution Level Predictor")
st.markdown("Predict AQI (Air Quality Index) based on temperature, traffic, and industrial activity using a machine learning model trained on historical data and current data from aqi.in.")

# --- Load and preprocess historical data ---
X_train, X_test, y_train, y_test = load_and_preprocess_data("delhi_air_quality.csv", "dubai_air_quality.csv") # Replace with your actual file paths

if X_train is not None:
    # --- Train the model ---
    model = LinearRegression() # You can change this to a different model
    model.fit(X_train, y_train)

    # --- Fetch current data from aqi.in and make prediction ---
    st.sidebar.header("Current Conditions (Dubai)")
    # --- We can now directly use the API key in the function ---
    current_data = get_current_data_aqi_in(city_name="Dubai")
    if current_data is not None:
        # --- Handle cases where temperature might not be available ---
        if current_data[0][0] is not None:
            try:
                predicted_aqi = model.predict(current_data)[0]
                st.subheader("Predicted Air Quality Index (Current - Dubai)")
                st.success(f" **{predicted_aqi:.2f} AQI**")
            except Exception as e:
                st.error(f"Error making prediction: {e}")
        else:
            st.warning("Temperature data not available from aqi.in. Prediction might be less accurate.")

    # --- Optionally keep the Actual vs Predicted plot ---
    st.subheader("Actual vs Predicted (Test Set)")
    fig, ax = plt.subplots()
    ax.scatter(y_test, y_pred, alpha=0.6, color='green')
    ax.plot([min(y_test), max(y_test)], [min(y_test), max(y_test)], 'r--')
    ax.set_xlabel("Actual AQI")
    ax.set_ylabel("Predicted AQI")
    st.pyplot(fig)

else:
    st.warning("Please ensure historical data files are available.")
