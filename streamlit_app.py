import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

# --- Function to load and preprocess historical data ---
@st.cache_data
def load_and_preprocess_data(delhi_data_path, dubai_data_path):
    try:
        delhi_df = pd.read_csv(delhi_data_path)
        dubai_df = pd.read_csv(dubai_data_path)
        # --- Data cleaning, feature selection, and merging ---
        # This will depend heavily on the structure of your data
        combined_df = pd.concat([delhi_df, dubai_df], ignore_index=True)
        # --- Select relevant features and target variable ---
        X = combined_df[["temperature", "traffic_proxy", "industry_proxy"]] # Rename based on your actual columns
        y = combined_df["aqi"] # Rename based on your actual column
        return train_test_split(X, y, test_size=0.2, random_state=42)
    except FileNotFoundError:
        st.error("Error: Historical data files not found.")
        return None, None, None, None

# --- Function to fetch current data (Conceptual) ---
def get_current_data():
    # --- Replace this with your actual API calls ---
    # Example using a placeholder:
    current_temp = 35 # Replace with actual API call
    current_traffic = 7 # Replace with actual API call (if available)
    current_industry = 6 # Replace with actual API call (if available)
    return np.array([[current_temp, current_traffic, current_industry]])

st.set_page_config(page_title="AI Air Pollution Predictor", layout="centered")
st.title("AI Air Pollution Level Predictor")
st.markdown("Predict AQI (Air Quality Index) based on temperature, traffic, and industrial activity using a machine learning model trained on historical data from Delhi and Dubai and current data.")

# --- Load and preprocess historical data ---
X_train, X_test, y_train, y_test = load_and_preprocess_data("delhi_air_quality.csv", "dubai_air_quality.csv") # Replace with your actual file paths

if X_train is not None:
    # --- Train the model ---
    model = LinearRegression() # You can change this to a different model
    model.fit(X_train, y_train)

    # --- Fetch current data and make prediction ---
    st.sidebar.header("Current Conditions (Dubai)")
    current_data = get_current_data()
    if current_data is not None:
        try:
            predicted_aqi = model.predict(current_data)[0]
            st.subheader("Predicted Air Quality Index (Current - Dubai)")
            st.success(f" **{predicted_aqi:.2f} AQI**")
        except Exception as e:
            st.error(f"Error making prediction: {e}")

    # --- Optionally keep the Actual vs Predicted plot if you find it useful for debugging ---
    st.subheader("Actual vs Predicted (Test Set)")
    fig, ax = plt.subplots()
    ax.scatter(y_test, y_pred, alpha=0.6, color='green')
    ax.plot([min(y_test), max(y_test)], [min(y_test), max(y_test)], 'r--')
    ax.set_xlabel("Actual AQI")
    ax.set_ylabel("Predicted AQI")
    st.pyplot(fig)

else:
    st.warning("Please ensure historical data files are available.")
