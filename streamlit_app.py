import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

st.set_page_config(page_title="Air Pollution AI", layout="centered")

st.title("🌫️ Air Pollution Level Predictor")
st.write("Built by Rahul – Predict PM2.5 based on real-world factors and live city data.")

# ----------- DUMMY DATASET -----------
@st.cache_data
def generate_data():
    np.random.seed(42)
    data = {
        'temperature': np.random.normal(30, 5, 100),
        'traffic_level': np.random.randint(1, 10, 100),
        'industrial_activity': np.random.randint(1, 10, 100)
    }
    df = pd.DataFrame(data)
    df['pm25'] = (
        0.5 * df['temperature']
        + 2 * df['traffic_level']
        + 3 * df['industrial_activity']
        + np.random.normal(0, 5, 100)
    )
    return df

df = generate_data()

# ----------- MODEL TRAINING -----------
X = df[['temperature', 'traffic_level', 'industrial_activity']]
y = df['pm25']
model = LinearRegression()
model.fit(X, y)

# ----------- SIDEBAR INPUTS -----------
st.sidebar.header("Adjust Inputs for Prediction")
temperature = st.sidebar.slider("🌡️ Temperature (°C)", 0, 50, 30)
traffic = st.sidebar.slider("🚗 Traffic Level (1-10)", 1, 10, 5)
industry = st.sidebar.slider("🏭 Industrial Activity (1-10)", 1, 10, 5)

input_data = np.array([[temperature, traffic, industry]])
prediction = model.predict(input_data)[0]

st.subheader("📊 Predicted PM2.5 Level")
st.metric(label="μg/m³", value=f"{prediction:.2f}")

# ----------- LIVE AIR QUALITY API -----------
st.subheader("🌍 Live PM2.5 from a Real City")
city = st.text_input("Enter city name (e.g. Delhi, Mumbai, London)", "Delhi")

if city:
    try:
        url = f"https://api.openaq.org/v2/latest?city={city}&parameter=pm25"
        response = requests.get(url).json()
        live_pm = response['results'][0]['measurements'][0]['value']
        unit = response['results'][0]['measurements'][0]['unit']
        st.success(f"Live PM2.5 in {city}: {live_pm} {unit}")
    except Exception as e:
        st.error("Couldn't fetch data. Try a valid city.")

# ----------- CHART -----------
st.subheader("📈 Prediction Chart Based on Traffic")
traffic_range = np.arange(1, 11)
predicted_pm25 = [
    model.predict([[temperature, t, industry]])[0] for t in traffic_range
]

fig, ax = plt.subplots()
ax.plot(traffic_range, predicted_pm25, marker='o', color='orange')
ax.set_xlabel("Traffic Level")
ax.set_ylabel("Predicted PM2.5 (µg/m³)")
ax.set_title("Effect of Traffic on PM2.5 at fixed Temp & Industry")
st.pyplot(fig)

# ----------- OPTIONAL: SHOW RAW DATA -----------
if st.checkbox("🔍 Show Training Data"):
    st.write(df.head())
pip install streamlit pandas numpy matplotlib scikit-learn requests
streamlit run streamlit_app.py



